import React, { useEffect, useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

const App = () => {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    // Запрос на FastAPI для получения списка рецептов
    axios
      .get("http://127.0.0.1:8000/recipes")
      .then((response) => {
        setRecipes(response.data); // Сохраняем рецепты в состояние
      })
      .catch((error) => {
        console.error("Ошибка при получении рецептов", error);
      });
  }, []);

  return (
    <div className="container text-center mt-5">
      <h1 className="display-4 text-primary">🍹 Коктейльный гид</h1>
      <div className="row mt-4">
        {recipes.map((recipe) => (
          <div className="col-md-4" key={recipe.id}>
            <div className="card cocktail-card shadow-sm">
              <div className="card-body">
                <h5 className="card-title">{recipe.name}</h5>
                <p className="card-text">{recipe.instruction}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
