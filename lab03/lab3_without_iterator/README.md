# Отчёт по лабораторной работе

## Тема
Сравнение двух реализаций одного и того же приложения:
- версия **без паттерна Итератор** (этот каталог),
- версия **с паттерном Итератор** (исходный проект в родительской папке).

Цель сравнения: наглядно показать, как паттерн Итератор упрощает поддержку и развитие кода при работе со списками рекомендаций.

---

## 1. Идея проекта

Приложение хранит пользователей и отображает их как точки на координатной плоскости.

У пользователя есть поля:
- имя,
- фамилия,
- список друзей,
- интересы из фиксированного набора категорий.

Точка пользователя (`x`, `y`, `user_id`) вычисляется так:
- главная привязка к друзьям (среднее по координатам друзей),
- небольшое смещение по интересам,
- фамилия и имя в текущей модели координат не влияют.

Сценарий для пользователя:
- слева форма регистрации,
- справа координатная плоскость с точками,
- слева же таблица 10 ближайших пользователей,
- дополнительный блок пошагового просмотра рекомендаций.

Технологии одинаковые в обеих версиях:
- Python,
- Tkinter,
- без `yield`, без внешних библиотек.

---

## 2. Реализация без паттерна (этот каталог)

Структура:
- `main.py` — точка входа.
- `social_lab_no_iterator/models.py` — модели и преобразование User -> Point.
- `social_lab_no_iterator/point_space.py` — хранение пользователей и вычисление рекомендаций.
- `social_lab_no_iterator/gui.py` — весь интерфейс, таблица, ручной пошаговый просмотр списка.

Ключевая идея версии без паттерна:
- `UserPointSpaceNoIterator.get_recommendations(...)` сразу возвращает готовый `list[Recommendation]`.
- GUI сам хранит состояние обхода: список + индекс (`demo_recommendations`, `demo_index`).

---

## 3. Проблема, которую решает паттерн

### 3.1 Неприятный кусок №1: ручное состояние обхода в GUI

Из `social_lab_no_iterator/gui.py`:

```python
self.demo_recommendations = self.space.get_recommendations(self.current_user_id, limit=10)
self.demo_index = 0

if self.demo_index >= total:
    self.demo_status_var.set(f"List exhausted at {self.demo_index}/{total}.")
    return

recommendation = self.demo_recommendations[self.demo_index]
self.demo_index += 1
```

Почему это плохо:
- GUI вынужден знать детали обхода коллекции.
- Состояние (`index`, `total`, сброс, конец списка) размазано по нескольким методам.
- Легко получить баг при изменении логики (например, забыли сбросить индекс при смене базового пользователя).

### 3.2 Неприятный кусок №2: дублирование получения рекомендаций

Из `social_lab_no_iterator/gui.py`:

```python
recommendations = self.space.get_recommendations(self.current_user_id, limit=10)
for recommendation in recommendations:
    ...
```

и в другом месте снова:

```python
self.demo_recommendations = self.space.get_recommendations(self.current_user_id, limit=10)
self.demo_index = 0
```

Почему это плохо:
- Повторяется один и тот же запрос данных.
- При усложнении фильтров/сортировок возрастает риск рассинхронизации.
- Клиентский код (GUI) знает слишком много о способе обхода коллекции.

### 3.3 Неприятный кусок №3: нет единой абстракции обхода

Из `social_lab_no_iterator/point_space.py`:

```python
def get_recommendations(self, reference_user_id: int, limit: int = 10) -> list[Recommendation]:
    ...
    recommendations.sort(key=lambda item: (item.distance, item.user.user_id))
    if limit >= 0:
        return recommendations[:limit]
    return recommendations
```

Почему это плохо:
- Возвращается «сырой» список, а дальше каждый клиент обходит как хочет.
- Труднее контролировать единое поведение `next/has_next/reset`.
- Нет стандартизированного контракта обхода.

---

## 4. Решение с паттерном Итератор (исходная версия)

В исходной версии есть отдельная абстракция и реализация итератора.

### 4.1 Контракт итератора

Из `social_lab/iterator_pattern.py`:

```python
class Iterator(ABC, Generic[T]):
    @abstractmethod
    def has_next(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def next(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError
```

Плюс конкретная реализация:

```python
class NearestUsersIterator(Iterator[Recommendation]):
    def __init__(self, recommendations: Sequence[Recommendation]) -> None:
        self._recommendations = list(recommendations)
        self._index = 0

    def has_next(self) -> bool:
        return self._index < len(self._recommendations)

    def next(self) -> Recommendation:
        if not self.has_next():
            raise StopIteration("No more recommendations in iterator.")
        current = self._recommendations[self._index]
        self._index += 1
        return current

    def reset(self) -> None:
        self._index = 0
```

### 4.2 Агрегат создаёт итератор

Из `social_lab/point_space.py`:

```python
def create_iterator(self, reference_user_id: int, limit: int = 10) -> NearestUsersIterator:
    ...
    recommendations.sort(key=lambda item: (item.distance, item.user.user_id))
    if limit >= 0:
        recommendations = recommendations[:limit]
    return NearestUsersIterator(recommendations)
```

### 4.3 GUI работает через единый интерфейс

Из `social_lab/gui.py`:

```python
iterator = self.space.create_iterator(self.current_user_id, limit=10)
while iterator.has_next():
    recommendation = iterator.next()
    ...
```

И для пошаговой демонстрации:

```python
self.iterator_demo = self.space.create_iterator(self.current_user_id, limit=10)
...
if not self.iterator_demo.has_next():
    ...
recommendation = self.iterator_demo.next()
...
self.iterator_demo.reset()
```

Почему это лучше:
- Клиент не управляет внутренностями обхода вручную.
- Логика `next/has_next/reset` сосредоточена в одном месте.
- Проще тестировать и расширять (другой порядок обхода, фильтрация, лимиты).

---

## 5. Объяснение паттерна Итератор

Паттерн Итератор нужен, когда нужно обходить коллекцию, не раскрывая её внутреннее устройство клиенту.

Участники паттерна в этом проекте:
- `Aggregate` — интерфейс объекта-коллекции, который умеет создавать итератор.
- `UserPointSpace` — конкретная коллекция пользователей/точек.
- `Iterator` — интерфейс обхода (`has_next`, `next`, `reset`).
- `NearestUsersIterator` — конкретный обход рекомендаций по близости.
- GUI — клиент, который использует только интерфейс итератора.

Главный эффект:
- уменьшается связность GUI и бизнес-логики,
- повышается читаемость,
- проще поддержка при изменениях.

---

## 6. Заключение по лабораторной работе

1. Одна и та же задача успешно реализуется как без паттерна, так и с паттерном Итератор.
2. Версия без паттерна работоспособна, но содержит ручное управление обходом списка и повышенную связность в GUI.
3. Версия с паттерном даёт более чистую архитектуру: обход стандартизирован, клиентский код проще и безопаснее в сопровождении.
4. Для учебной цели сравнение показало ценность паттерна на реальном интерфейсном сценарии (таблица + пошаговый просмотр кандидатов).

---

## Запуск версии без паттерна

Из папки `lab3_without_iterator`:

```bash
python main.py
```

Если используется локальное окружение:

```bash
.\\.venv\\Scripts\\python.exe main.py
```
