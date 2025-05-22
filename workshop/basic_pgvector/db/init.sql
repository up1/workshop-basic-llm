CREATE EXTENSION vector;

CREATE TABLE documents (
    id int PRIMARY KEY,
    title text NOT NULL
);

CREATE TABLE document_embeddings (
    id int PRIMARY KEY,
    embedding vector(1536) NOT NULL
);

CREATE INDEX document_embeddings_embedding_idx ON document_embeddings 
USING hnsw (embedding vector_l2_ops);

INSERT INTO documents (id, title) VALUES
(1, 'Wireless Noise Cancelling Headphones'),
(2, '4K Ultra HD Smart LED TV'),
(3, 'Stainless Steel Electric Kettle'),
(4, 'Bluetooth Portable Speaker'),
(5, 'Ergonomic Office Chair'),
(6, 'Smartphone with Triple Camera'),
(7, 'Gaming Mechanical Keyboard'),
(8, 'Fitness Activity Tracker'),
(9, 'Home Espresso Coffee Machine'),
(10, 'Robot Vacuum Cleaner');

-- INSERT INTO documents VALUES ('1', 'The weather is lovely today.');
-- INSERT INTO documents VALUES ('2', 'It s so sunny outside!');
-- INSERT INTO documents VALUES ('3', 'He drove to the stadium.');
