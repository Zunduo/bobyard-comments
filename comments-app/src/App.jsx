import { useEffect, useState } from 'react'
import CommentCard from './components/CommentCard'
import { listComments, addComment, editComment, deleteComment } from './api/comments'
import './App.css'

function App() {
  const [comments, setComments] = useState([]);
  const [newText, setNewText] = useState("");
  const [editingId, setEditingId] = useState(null);

  async function refresh() {
    const data = await listComments();
    setComments(data);
  }

  useEffect(() => {
    refresh()
  }, []);
  
  async function handleAdd(e) {
    e.preventDefault();
    if(!newText) return;
    try {
      await addComment(newText);
      await refresh();
      setNewText("");
    } catch (error) {
      console.error(error);
    }
  }
  async function handleSaveEdit(id, text) {
    try {
      await editComment(id, text);
      await refresh();
    } catch (error) {
      console.error(error);
    }
  }
  async function handleDelete(id) {
    try {
      await deleteComment(id);
      await refresh();
    } catch (error) {
      console.error(error);
    }
  }

  return (

    <div className="page">
      <header className="header">
        <h1>Comments</h1>
        <p className="subtitle">Bobyard Comments UI</p>
      </header>
      <form onSubmit={handleAdd}>
        <textarea value={newText} onChange={(e) => setNewText(e.target.value)} placeholder="Write a comment..." rows={3} />
        <button type="submit" disabled={!newText}>Add comment</button>
      </form>
      <section className="list">
        {comments.map((comment) => (
          <CommentCard key={comment.id} comment={comment} onSaveEdit={handleSaveEdit} onDelete={handleDelete} editingId={editingId} setEditingId={setEditingId} />
        ))}
      </section>
    </div>
  )
}

export default App;
