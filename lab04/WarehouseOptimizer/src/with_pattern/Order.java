package with_pattern;

import java.util.ArrayList;
import java.util.List;

public class Order {
    private final String orderId;
    private final String pickerName;
    private List<ShelfPoint> pointsToVisit;

    public Order(String orderId, String pickerName) {
        this.orderId = orderId;
        this.pickerName = pickerName;
        this.pointsToVisit = new ArrayList<>();
    }

    public void addPoint(ShelfPoint point) {
        pointsToVisit.add(point);
    }

    public List<ShelfPoint> getPointsToVisit() {
        return new ArrayList<>(pointsToVisit);
    }

    /**
     * Оптимизация маршрута "жадным" алгоритмом (ближайший сосед).
     * Начальная точка условно (0,0).
     */
    public List<ShelfPoint> optimizeRoute() {
        if (pointsToVisit.isEmpty()) {
            return new ArrayList<>();
        }

        List<ShelfPoint> unvisited = new ArrayList<>(pointsToVisit);
        List<ShelfPoint> optimized = new ArrayList<>();
        
        ShelfPoint current = new ShelfPoint(0, 0); // Старт
        
        while (!unvisited.isEmpty()) {
            ShelfPoint nearest = null;
            int minDistance = Integer.MAX_VALUE;
            
            for (ShelfPoint p : unvisited) {
                int dist = current.manhattanDistanceTo(p);
                if (dist < minDistance) {
                    minDistance = dist;
                    nearest = p;
                }
            }
            
            optimized.add(nearest);
            unvisited.remove(nearest);
            current = nearest;
        }
        
        return optimized;
    }
    
    public int calculateTotalDistance(List<ShelfPoint> route) {
        int total = 0;
        ShelfPoint current = new ShelfPoint(0, 0);
        for (ShelfPoint p : route) {
            total += current.manhattanDistanceTo(p);
            current = p;
        }
        return total;
    }
}
