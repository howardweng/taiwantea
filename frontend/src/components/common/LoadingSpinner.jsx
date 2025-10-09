import './LoadingSpinner.module.css';

function LoadingSpinner({ size = 'medium' }) {
  return (
    <div className={`spinner spinner-${size}`} role="status" aria-label="Loading">
      <div className="spinner-circle"></div>
    </div>
  );
}

export default LoadingSpinner;
