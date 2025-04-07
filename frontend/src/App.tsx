import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const res = await axios.post('http://localhost:8000/ask', { question });
      setResponse(res.data.response);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        setError(error.response?.data?.detail || 'Error fetching response');
      } else {
        setError('An unexpected error occurred');
      }
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>📊 AI Business Assistant</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Ask your business question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Ask'}
        </button>
      </form>
      {error && <p className="error">❌ {error}</p>}
      {response && <p className="response">🧠 Response: {response}</p>}
    </div>
  );
}

export default App;