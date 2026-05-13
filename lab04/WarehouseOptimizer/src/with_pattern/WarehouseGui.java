package with_pattern;

import javax.swing.*;
import java.awt.*;
import java.util.List;

public class WarehouseGui extends JFrame {
    private final int GRID_SIZE = 10;
    private final Order currentOrder;
    private List<ShelfPoint> optimizedRoute = null;
    
    private final JPanel gridPanel;
    private final JTextArea logArea;

    public WarehouseGui() {
        super("Оптимизатор маршрута (с Value Object)");
        this.currentOrder = new Order("ORD-001", "Иван");
        
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
                
                try {
                    currentOrder.addPoint(new ShelfPoint(x, y));
                    optimizedRoute = null; // сброс маршрута при добавлении
                    logArea.append("Добавлена точка: (" + x + ", " + y + ")\n");
                    gridPanel.repaint();
                } catch (IllegalArgumentException e) {
                    JOptionPane.showMessageDialog(gridPanel, e.getMessage());
                }
            }
        });

        logArea = new JTextArea(10, 30);
        logArea.setEditable(false);
        
        JButton optimizeBtn = new JButton("Оптимизировать маршрут");
        optimizeBtn.addActionListener(e -> {
            optimizedRoute = currentOrder.optimizeRoute();
            int totalDist = currentOrder.calculateTotalDistance(optimizedRoute);
            
            logArea.append("=== Маршрут построен ===\n");
            logArea.append("Общая длина: " + totalDist + " м.\n");
            
            ShelfPoint curr = new ShelfPoint(0, 0);
            for (ShelfPoint p : optimizedRoute) {
                logArea.append("Иди из (" + curr.x() + "," + curr.y() + ") в (" + p.x() + "," + p.y() + ") - расст: " + curr.manhattanDistanceTo(p) + "\n");
                curr = p;
            }
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
        for (ShelfPoint p : currentOrder.getPointsToVisit()) {
            g.fillRect(p.x() * cellW + 2, p.y() * cellH + 2, cellW - 4, cellH - 4);
        }

        if (optimizedRoute != null && !optimizedRoute.isEmpty()) {
            g.setColor(Color.RED);
            Graphics2D g2 = (Graphics2D) g;
            g2.setStroke(new BasicStroke(3));
            
            int prevX = 0 * cellW + cellW / 2; // Start at (0,0)
            int prevY = 0 * cellH + cellH / 2;
            
            for (ShelfPoint p : optimizedRoute) {
                int currX = p.x() * cellW + cellW / 2;
                int currY = p.y() * cellH + cellH / 2;
                
                // Manhattan path drawing
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
