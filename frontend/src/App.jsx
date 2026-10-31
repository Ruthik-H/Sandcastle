
import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [environments, setEnvironments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function fetchEnvironments() {
      try {
        const response = await fetch(
          'http://127.0.0.1:8000/environments'
        )

        if (!response.ok) {
          throw new Error('Failed to fetch environments')
        }

        const data = await response.json()

        setEnvironments(data.environments)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchEnvironments()
  }, [])

  return (
    <div style={{ padding: '30px', color: '#e5e7eb' }}>
      <h1>Sandcastle Dashboard</h1>
      <p>Preview Environment Management</p>

      <h2>Preview Environments</h2>

      {loading && <p>Loading environments...</p>}

      {error && <p>Error: {error}</p>}

      {!loading && !error && environments.map((env) => (
        <div
          key={env.id}
          style={{
            padding: '16px',
            marginBottom: '12px',
            background: '#172033',
            borderRadius: '8px'
          }}
        >
          <h3>{env.repository}</h3>
          <p>Pull Request: #{env.pull_request}</p>
          <p>Status: {env.status}</p>
        </div>
      ))}
    </div>
  )
}

export default App
