import React, { useEffect, useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
    const [recipes, setRecipes] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/recipes") // Запрос к API FastAPI
            .then(response => {
                setRecipes(response.data); // Обновляем состояние
            })
            .catch(error => {
                console.error("Ошибка при загрузке рецептов:", error);
            });
    }, []);

    return (
        <div className="container mt-5">
            <h1 className="text-center">📜 Рецепты коктейлей</h1>
            <div className="row">
                {recipes.map((recipe) => (
                    <div key={recipe.id} className="col-md-4">
                        <div className="card mb-4">
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
}

export default App;
