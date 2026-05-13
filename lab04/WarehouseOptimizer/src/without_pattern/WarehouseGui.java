package without_pattern;

import javax.swing.*;
import java.awt.*;

public class WarehouseGui extends JFrame {
    private final int GRID_SIZE = 10;
    private Order currentOrder;
    private int[][] optimizedRoute = null;
    
    private JPanel gridPanel;
    private JTextArea logArea;

    public WarehouseGui() {
        super("Оптимизатор маршрута (БЕЗ Value Object)");
        this.currentOrder = new Order("ORD-002", "Петр");
        
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(800, 600);
        setLayout(new BorderLayout());

        gridPanel = new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                drawGridAndRoute(g);
            }
        };
        gridPanel.addMouseListener(new java.awt.event.MouseAdapter() {
            @Override
            public void mouseClicked(java.awt.event.MouseEvent evt) {
                int cellWidth = gridPanel.getWidth() / GRID_SIZE;
                int cellHeight = gridPanel.getHeight() / GRID_SIZE;
                int x = evt.getX() / cellWidth;
                int y = evt.getY() / cellHeight;
                
                // Валидация размазана по коду GUI
                if (x < 0 || x > 50 || y < 0 || y > 50) {
                    JOptionPane.showMessageDialog(gridPanel, "Неверные координаты");
                    return;
                }
                
                currentOrder.addPoint(x, y);
                optimizedRoute = null; // сброс
                logArea.append("Добавлена точка: (" + x + ", " + y + ")\n");
                gridPanel.repaint();
            }
        });

        logArea = new JTextArea(10, 30);
        logArea.setEditable(false);
        
        JButton optimizeBtn = new JButton("Оптимизировать маршрут");
        optimizeBtn.addActionListener(e -> {
            optimizedRoute = currentOrder.optimizeRoute();
            
            int totalDist = 0;
            int currX = 0;
            int currY = 0;
            
            logArea.append("=== Маршрут построен ===\n");
            for (int i = 0; i < optimizedRoute.length; i++) {
                int nextX = optimizedRoute[i][0];
                int nextY = optimizedRoute[i][1];
                
                // Опять дублирование расчета расстояния!
                int dist = Math.abs(currX - nextX) + Math.abs(currY - nextY);
                totalDist += dist;
                
                logArea.append("Иди из (" + currX + "," + currY + ") в (" + nextX + "," + nextY + ") - расст: " + dist + "\n");
                
                currX = nextX;
                currY = nextY;
            }
            logArea.insert("Общая длина: " + totalDist + " м.\n", 25);
            gridPanel.repaint();
        });

        add(gridPanel, BorderLayout.CENTER);
        
        JPanel rightPanel = new JPanel(new BorderLayout());
        rightPanel.add(new JScrollPane(logArea), BorderLayout.CENTER);
        rightPanel.add(optimizeBtn, BorderLayout.SOUTH);
        
        add(rightPanel, BorderLayout.EAST);
    }

    private void drawGridAndRoute(Graphics g) {
        int w = gridPanel.getWidth();
        int h = gridPanel.getHeight();
        int cellW = w / GRID_SIZE;
        int cellH = h / GRID_SIZE;

        g.setColor(Color.LIGHT_GRAY);
        for (int i = 0; i <= GRID_SIZE; i++) {
            g.drawLine(i * cellW, 0, i * cellW, h);
            g.drawLine(0, i * cellH, w, i * cellH);
        }

        g.setColor(Color.BLUE);
        for (int i = 0; i < currentOrder.getPointsX().size(); i++) {
            int px = currentOrder.getPointsX().get(i);
            int py = currentOrder.getPointsY().get(i);
            g.fillRect(px * cellW + 2, py * cellH + 2, cellW - 4, cellH - 4);
        }

        if (optimizedRoute != null && optimizedRoute.length > 0) {
            g.setColor(Color.RED);
            Graphics2D g2 = (Graphics2D) g;
            g2.setStroke(new BasicStroke(3));
            
            int prevX = cellW / 2; // (0,0) center
            int prevY = cellH / 2;
            
            for (int[] p : optimizedRoute) {
                int currX = p[0] * cellW + cellW / 2;
                int currY = p[1] * cellH + cellH / 2;
                
                g2.drawLine(prevX, prevY, currX, prevY);
                g2.drawLine(currX, prevY, currX, currY);
                
                prevX = currX;
                prevY = currY;
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new WarehouseGui().setVisible(true);
        });
    }
}
