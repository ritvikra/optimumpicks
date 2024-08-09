import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [odds, setOdds] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://localhost:5000/odds')
      .then(response => {
        setOdds(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("There was an error fetching the odds!", error);
        setLoading(false);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Sportsbook Odds</h1>
      </header>
      <main>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Sportsbook</th>
                <th>Odds</th>
              </tr>
            </thead>
            <tbody>
              {odds.map((odd, index) => (
                <tr key={index}>
                  <td>{odd.sportsbook}</td>
                  <td>{odd.odds}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </main>
    </div>
  );
};

export default App;