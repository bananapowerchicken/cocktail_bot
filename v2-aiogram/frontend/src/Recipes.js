import React, { useState, useEffect } from "react";
import axios from "axios";

const RecipeList = () => {
    const [recipes, setRecipes] = useState([]);

    useEffect(() => {
        axios.get("http://localhost:8000/recipes")
            .then((response) => {
                setRecipes(response.data);
            })
            .catch((error) => {
                console.error("Ошибка при загрузке рецептов:", error);
            });
    }, []);

    return (
        <div>
            <h2>📜 Список коктейлей</h2>
            {recipes.map((recipe) => (
                <div key={recipe.id} style={{ border: "1px solid #ccc", padding: "10px", marginBottom: "10px" }}>
                    <h3>{recipe.name}</h3>
                    <p><strong>Инструкция:</strong> {recipe.instruction}</p>
                    <h4>🧪 Ингредиенты:</h4>
                    <ul>
                        {recipe.ingredients.map((ing, index) => (
                            <li key={index}>{ing.name} - {ing.quantity} {ing.unit}</li>
                        ))}
                    </ul>
                </div>
            ))}
        </div>
    );
};

export default RecipeList;
