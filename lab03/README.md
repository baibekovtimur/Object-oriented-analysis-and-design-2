# Лабораторная работа: сравнение реализации с паттерном Итератор и без него

## Структура проекта

```text
lab3/
  lab3_iterator/
    main.py
    social_lab/
      models.py
      point_space.py
      iterator_pattern.py
      gui.py
  lab3_without_iterator/
    main.py
    social_lab_no_iterator/
      models.py
      point_space.py
      gui.py
  README.md
```

## 1. Идея проекта

Приложение моделирует пользователей социальной сети и показывает их как точки на координатной плоскости.

Каждый пользователь имеет:
- имя,
- фамилию,
- список друзей,
- интересы (из заданных категорий).

Преобразование пользователя в точку выполняется по смысловым признакам:
- основной вклад дают друзья,
- интересы вносят небольшое смещение,
- фамилия и имя в текущей модели координат не участвуют.

Сценарий пользователя:
1. Слева заполняется форма регистрации.
2. Справа отображается координатное поле с точками пользователей.
3. Слева показывается таблица из 10 ближайших пользователей.
4. Есть пошаговый просмотр рекомендаций (демонстрация обхода коллекции).

## 2. Проблема, которую должен решить паттерн

Нужно не только получить список рекомендаций, но и удобно обходить его в разных режимах:
- полный обход (заполнение таблицы),
- пошаговый обход (кнопка «следующий»),
- сброс позиции обхода,
- единая логика окончания коллекции.

Если паттерна нет, клиентский код (GUI) начинает вручную хранить состояние обхода и дублировать логику.

## 3. Реализация без паттерна (lab3_without_iterator)

В версии без паттерна агрегат возвращает обычный список рекомендаций.

### 3.1. Фрагменты кода без паттерна

Источник: `lab3_without_iterator/social_lab_no_iterator/point_space.py`

```python
def get_recommendations(self, reference_user_id: int, limit: int = 10) -> list[Recommendation]:
    ...
    recommendations.sort(key=lambda item: (item.distance, item.user.user_id))
    if limit >= 0:
        return recommendations[:limit]
    return recommendations
```

Источник: `lab3_without_iterator/social_lab_no_iterator/gui.py`

```python
self.demo_recommendations = self.space.get_recommendations(self.current_user_id, limit=10)
self.demo_index = 0

if self.demo_index >= total:
    self.demo_status_var.set(f"List exhausted at {self.demo_index}/{total}.")
    return

recommendation = self.demo_recommendations[self.demo_index]
self.demo_index += 1
```

### 3.2. Почему это плохо

1. GUI хранит состояние обхода (`demo_recommendations`, `demo_index`), хотя это обязанность механизма итерации.
2. Логика обхода размазывается по нескольким методам (`_prepare_manual_demo`, `_manual_next`, `_manual_reset`).
3. Легко допустить ошибки состояния при доработках (забыть сброс индекса, обработку конца списка и т.д.).
4. Появляется повторное получение одной и той же коллекции для разных частей интерфейса.

## 4. Решение с паттерном Итератор (lab3_iterator)

В версии с паттерном введены явные роли: `Iterator`, `Aggregate`, конкретный итератор и конкретный агрегат.

### 4.1. Контракт итератора

Источник: `lab3_iterator/social_lab/iterator_pattern.py`

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

### 4.2. Конкретный итератор

Источник: `lab3_iterator/social_lab/iterator_pattern.py`

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

### 4.3. Агрегат создаёт итератор

Источник: `lab3_iterator/social_lab/point_space.py`

```python
def create_iterator(self, reference_user_id: int, limit: int = 10) -> NearestUsersIterator:
    ...
    recommendations.sort(key=lambda item: (item.distance, item.user.user_id))
    if limit >= 0:
        recommendations = recommendations[:limit]
    return NearestUsersIterator(recommendations)
```

### 4.4. GUI работает через единый интерфейс обхода

Источник: `lab3_iterator/social_lab/gui.py`

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

### 4.5. Почему это лучше

1. GUI не знает внутренности обхода коллекции.
2. Состояние итерации инкапсулировано в одном объекте.
3. Контракт `has_next/next/reset` единый и предсказуемый.
4. Проще менять стратегию обхода и переиспользовать её в других клиентах.

## 5. Объяснение паттерна Итератор на примере проекта

Итератор позволяет обойти коллекцию, не раскрывая клиенту, как именно она устроена.

Роли в этой лабораторной:
- `Aggregate` — интерфейс коллекции, которая умеет создавать итератор.
- `UserPointSpace` — конкретная коллекция пользователей/точек.
- `Iterator` — интерфейс обхода.
- `NearestUsersIterator` — конкретный обход рекомендаций по возрастанию дистанции.
- `SocialLabApp` — клиент, использующий только интерфейс итератора.

Важно: реализация выполнена без `yield`; вся логика итерации явно контролируется через индекс внутри класса итератора.

## 6. Заключение по лабораторной работе

1. Оба варианта решают одну и ту же пользовательскую задачу.
2. Вариант без паттерна быстрее написать, но сложнее поддерживать из-за ручного управления состоянием обхода.
3. Вариант с паттерном Итератор делает код чище: меньше связности, понятнее ответственность модулей, легче масштабировать.
4. Сравнение показывает практическую пользу паттернов проектирования не в абстракции, а в реальном GUI-сценарии.

## 7. Запуск проектов

### Версия с паттерном Итератор

```bash
cd lab3_iterator
python main.py
```

### Версия без паттерна Итератор

```bash
cd lab3_without_iterator
python main.py
```

При использовании виртуального окружения из корня проекта можно запускать так:

```bash
.\.venv\Scripts\python.exe .\lab3_iterator\main.py
.\.venv\Scripts\python.exe .\lab3_without_iterator\main.py
```
