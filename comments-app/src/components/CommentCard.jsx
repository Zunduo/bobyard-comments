function formatDate(isoTime) {
  const date = new Date(isoTime);
  return date.toLocaleDateString();
}

function CommentCard({
  comment,
  onSaveEdit,
  onDelete,
  editingId,
  setEditingId,
}) {
  const isEditing = editingId === comment.id;

  async function handleSave(e) {
    e.preventDefault();
    const text = e.target.elements.text.value.trim();
    if (!text || !onSaveEdit) return;
    await onSaveEdit(comment.id, text);
    setEditingId(null);
  }

  return (
    <article className="card">
      <div className="card-head">
        {comment.image ? (
          <img className="avatar" src={comment.image} alt="" />
        ) : (
          <div className="avatar placeholder">{comment.author?.[0] || "?"}</div>
        )}
        <div className="meta">
          <div>{comment.author}</div>
          <span className="sub">
            {formatDate(comment.date)} ~ {comment.likes} likes
          </span>
        </div>
        <div>
          {!isEditing && (
            <button type="button" onClick={() => setEditingId(comment.id)}>
              Edit
            </button>
          )}
          <button
            type="button"
            onClick={() => onDelete(comment.id)}
          >
            Delete
          </button>
        </div>
      </div>
      {isEditing ? (
        <form onSubmit={handleSave}>
          <textarea name="text" defaultValue={comment.text} />
          <button type="submit">Save</button>
          <button type="button" onClick={() => setEditingId(null)}>
              Cancel
          </button>
        </form>
      ) : (
        <p>{comment.text}</p>
      )}
    </article>
  );
}

export default CommentCard;
