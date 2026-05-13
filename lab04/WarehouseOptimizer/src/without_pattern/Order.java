package without_pattern;

import java.util.ArrayList;
import java.util.List;

public class Order {
    private String orderId;
    private String pickerName;
    
    // Плохой подход: параллельные списки примитивов
    private List<Integer> pointsX = new ArrayList<>();
    private List<Integer> pointsY = new ArrayList<>();

    public Order(String orderId, String pickerName) {
        this.orderId = orderId;
        this.pickerName = pickerName;
    }

    public void addPoint(int x, int y) {
        pointsX.add(x);
        pointsY.add(y);
    }

    public List<Integer> getPointsX() { return pointsX; }
    public List<Integer> getPointsY() { return pointsY; }

    /**
     * Оптимизация маршрута.
     * Логика расстояния продублирована и захардкожена.
     */
    public int[][] optimizeRoute() {
        if (pointsX.isEmpty()) return new int[0][2];

        List<Integer> unvisitedX = new ArrayList<>(pointsX);
        List<Integer> unvisitedY = new ArrayList<>(pointsY);
        
        int[][] optimized = new int[pointsX.size()][2];
        int count = 0;
        
        int currentX = 0;
        int currentY = 0;
        
        while (!unvisitedX.isEmpty()) {
            int nearestIdx = -1;
            int minDistance = Integer.MAX_VALUE;
            
            for (int i = 0; i < unvisitedX.size(); i++) {
                int px = unvisitedX.get(i);
                int py = unvisitedY.get(i);
                
                // Дублирование логики расчета Манхэттенского расстояния
                int dist = Math.abs(currentX - px) + Math.abs(currentY - py);
                if (dist < minDistance) {
                    minDistance = dist;
                    nearestIdx = i;
                }
            }
            
            int nextX = unvisitedX.get(nearestIdx);
            int nextY = unvisitedY.get(nearestIdx);
            
            optimized[count][0] = nextX;
            optimized[count][1] = nextY;
            count++;
            
            unvisitedX.remove(nearestIdx);
            unvisitedY.remove(nearestIdx);
            
            currentX = nextX;
            currentY = nextY;
        }
        
        return optimized;
    }
}
