import React, { useEffect, useState } from "react";
import axios from "axios";

const Recipes = () => {
    const [recipes, setRecipes] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/recipes")
            .then(response => {
                setRecipes(response.data);
            })
            .catch(error => {
                console.error("Ошибка при загрузке рецептов:", error);
            });
    }, []);

    return (
        <div style={{ textAlign: "center", padding: "20px" }}>
            <h1>📜 Рецепты коктейлей</h1>
            <ul style={{ listStyleType: "none", padding: 0 }}>
                {recipes.map(recipe => (
                    <li key={recipe.id} style={{ padding: "10px", borderBottom: "1px solid #ccc" }}>
                        <h3>{recipe.name}</h3>
                        <p>{recipe.instruction}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Recipes;
