import { useState } from 'react';
import './App.css';

function App() {
  const [recipeText, setRecipeText] = useState('');
  const [preferences, setPreferences] = useState('Hacerla más saludable');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    if (!recipeText.trim()) {
      setError('Debes ingresar el texto de la receta.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ recipe_text: recipeText, preferences }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Error en la API');
      }
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <h1>ModRecetas</h1>
        <p>Recetas más saludables con IA.</p>
      </header>

      <main className="content-grid">
        <section className="input-panel">
          <h2>Cargar receta</h2>
          <form onSubmit={handleSubmit}>
            <label>
              Texto de receta
              <textarea
                value={recipeText}
                onChange={(e) => setRecipeText(e.target.value)}
                rows="10"
                placeholder="Pega aquí la receta o descríbela..."
              />
            </label>
            <label>
              Preferencia
              <input
                value={preferences}
                onChange={(e) => setPreferences(e.target.value)}
              />
            </label>
            <button type="submit" disabled={loading}>
              {loading ? 'Procesando...' : 'Enviar'}
            </button>
            {error && <div className="alert error">{error}</div>}
          </form>
        </section>

        <section className="result-panel">
          <h2>Resultado</h2>
          {result ? (
            <div className="recipe-result">
              <div className="card">
                <h3>Ingredientes originales</h3>
                <ul>
                  {result.original_ingredients.map((item, index) => (
                    <li key={index}>
                      <span className="strike">{item.name}</span> — {item.quantity}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="card">
                <h3>Ingredientes modificados</h3>
                <ul>
                  {result.modified_ingredients.map((item, index) => (
                    <li key={index}>{item.name} — {item.quantity}</li>
                  ))}
                </ul>
              </div>

              <div className="card">
                <h3>Pasos modificados</h3>
                <ol>
                  {result.modified_steps.map((step, index) => (
                    <li key={index}>{step}</li>
                  ))}
                </ol>
              </div>

              {result.warnings.length > 0 && (
                <div className="alert warning">
                  <h4>Advertencias</h4>
                  <ul>
                    {result.warnings.map((warning, index) => (
                      <li key={index}>{warning}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <div className="placeholder">Envía una receta para ver la recomendación.</div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
