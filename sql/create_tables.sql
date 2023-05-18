CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    average_price NUMERIC
);

CREATE TABLE IF NOT EXISTS sells (
    id SERIAL PRIMARY KEY,
    shop VARCHAR(255),
    product_id INT,
    sell_date DATE,
    price NUMERIC,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION compute_mean_product()
  RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'DELETE' THEN
    UPDATE products
    SET average_price = (
      SELECT AVG(price)
      FROM sells
      WHERE sells.product_id = OLD.product_id
    )
    WHERE id = OLD.product_id;
  ELSE
    UPDATE products
    SET average_price = (
      SELECT AVG(price)
      FROM sells
      WHERE sells.product_id = NEW.product_id
    )
    WHERE id = NEW.product_id;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER compute_mean_insert_triger
AFTER INSERT ON sells
FOR EACH ROW
EXECUTE FUNCTION compute_mean_product();

CREATE TRIGGER compute_mean_update_triger
AFTER UPDATE ON sells
FOR EACH ROW
EXECUTE FUNCTION compute_mean_product();

CREATE TRIGGER compute_mean_delete_triger
AFTER DELETE ON sells
FOR EACH ROW
EXECUTE FUNCTION compute_mean_product();
