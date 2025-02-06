import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
    return (
        <div style={{ textAlign: "center", padding: "20px" }}>
            <h1>🍸 Добро пожаловать в коктейльный мир!</h1>
            <p>Выберите, что хотите сделать:</p>

            <div style={{ marginTop: "20px" }}>
                {/* Кнопка для перехода к рецептам */}
                <Link to="/recipes">
                    <button style={buttonStyle}>📜 Смотреть рецепты</button>
                </Link>
            </div>

            <div style={{ marginTop: "20px" }}>
                {/* Ссылка на Telegram-бота */}
                <a href="https://t.me/GimmeCocktail_bot" target="_blank" rel="noopener noreferrer">
                    <button style={buttonStyle}>🤖 Перейти в Telegram-бот</button>
                </a>
            </div>
        </div>
    );
};

// Стили кнопок
const buttonStyle = {
    padding: "12px 20px",
    fontSize: "16px",
    cursor: "pointer",
    backgroundColor: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "5px",
    textDecoration: "none",
    margin: "5px",
};

export default Home;