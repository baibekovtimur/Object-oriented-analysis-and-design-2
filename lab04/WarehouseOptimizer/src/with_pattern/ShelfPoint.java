package with_pattern;

import java.util.Objects;

/**
 * Value Object, представляющий координату стеллажа на складе.
 * Неизменяемый класс, инкапсулирует валидацию и расчет расстояния.
 */
public record ShelfPoint(int x, int y) {

    public ShelfPoint {
        if (x < 0 || x > 50 || y < 0 || y > 50) {
            throw new IllegalArgumentException("Координаты склада должны быть в диапазоне от 0 до 50");
        }
    }

    /**
     * Расчет Манхэттенского расстояния.
     */
    public int manhattanDistanceTo(ShelfPoint other) {
        return Math.abs(this.x - other.x) + Math.abs(this.y - other.y);
    }
}
