\connect ecommerce_db

-- Seed customer_schema.users
SET search_path = customer_schema;

INSERT INTO users (username, email, role) VALUES
('admin_user', 'admin@example.com', 'admin'),
('john_doe', 'john@example.com', 'user'),
('jane_smith', 'jane@example.com', 'user'),
('mod_sarah', 'sarah@example.com', 'moderator'),
('tech_support', 'support@example.com', 'support');

INSERT INTO profiles (user_id, first_name, last_name, phone, address) VALUES
(1, 'Admin', 'User', '555-0100', '123 Admin St, Tech City, TC 10001'),
(2, 'John', 'Doe', '555-0101', '456 Oak Lane, Springfield, SP 20002'),
(3, 'Jane', 'Smith', '555-0102', '789 Maple Ave, Rivertown, RT 30003'),
(4, 'Sarah', 'Johnson', '555-0103', '321 Pine Road, Hillside, HS 40004'),
(5, 'Tom', 'Support', '555-0104', '654 Tech Blvd, Support City, SC 50005');

-- Seed product_schema.categories and products
SET search_path = product_schema;

INSERT INTO categories (name, description) VALUES
('Electronics', 'Electronic devices and accessories'),
('Books', 'Physical and digital books'),
('Clothing', 'Apparel and accessories'),
('Home & Garden', 'Home improvement and garden supplies');

INSERT INTO products (category_id, name, description, price, stock) VALUES
(1, 'Smartphone Pro', '6.7-inch display, 256GB storage', 999.99, 50),
(1, 'Wireless Earbuds', 'Noise-canceling wireless earbuds', 149.99, 100),
(2, 'Python Programming', 'Comprehensive guide to Python', 49.99, 75),
(2, 'Data Science Basics', 'Introduction to data science', 39.99, 60),
(3, 'Classic T-Shirt', '100% cotton, multiple colors', 19.99, 200),
(3, 'Denim Jeans', 'Comfortable fit, dark wash', 59.99, 150),
(4, 'Garden Tools Set', '5-piece essential garden tools', 89.99, 30),
(4, 'Smart LED Bulb', 'WiFi-enabled multicolor LED', 29.99, 80);

-- Seed order_schema.orders and order_items
SET search_path = order_schema;

INSERT INTO orders (user_id, total_amount, status) VALUES
(2, 1149.98, 'completed'),
(3, 89.98, 'completed'),
(2, 149.99, 'pending'),
(4, 119.98, 'processing'),
(3, 209.97, 'completed');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 999.99),
(1, 2, 1, 149.99),
(2, 3, 1, 49.99),
(2, 4, 1, 39.99),
(3, 2, 1, 149.99),
(4, 5, 2, 19.99),
(4, 6, 1, 59.99),
(5, 7, 1, 89.99),
(5, 8, 4, 29.99);

-- Add some sample data analysis queries
CREATE OR REPLACE VIEW order_schema.order_summary AS
SELECT 
    o.order_id,
    u.username,
    COUNT(oi.order_item_id) as items_count,
    o.total_amount,
    o.status,
    o.order_date
FROM order_schema.orders o
JOIN customer_schema.users u ON o.user_id = u.user_id
JOIN order_schema.order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, u.username;