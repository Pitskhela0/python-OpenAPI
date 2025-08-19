USE student_room_db;

CREATE TABLE IF NOT EXISTS Rooms (
    room_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Students (
    student_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    birthday DATE NOT NULL,
    sex ENUM('M', 'F') NOT NULL,
    room_id INT,
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO Rooms (room_id, name) VALUES
    (101, 'Computer Science Lab'),
    (102, 'Mathematics Room'),
    (103, 'Physics Laboratory');

INSERT IGNORE INTO Students (student_id, name, birthday, sex, room_id) VALUES
    (1001, 'John Doe', '2000-05-15', 'M', 101),
    (1002, 'Jane Smith', '1999-12-03', 'F', 101),
    (1003, 'Mike Johnson', '2001-08-22', 'M', 102),
    (1004, 'Sarah Wilson', '2000-03-10', 'F', NULL);