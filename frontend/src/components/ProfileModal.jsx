import './ProfileModal.css';

export default function ProfileModal({ isLoggedIn, onClose, onLogout }) {
  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) onClose();
  };

  return (
    <div className="modal-overlay" onClick={handleOverlayClick}>
      <div className="modal">
        <button className="modal__close" onClick={onClose} aria-label="Close">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>

        {isLoggedIn ? (
          <>
            <h2 className="modal__title">Account</h2>
            <div className="modal__actions">
              <button className="modal__btn modal__btn--secondary">
                Profile
              </button>
              <button
                className="modal__btn modal__btn--danger"
                onClick={() => {
                  onLogout?.();
                  onClose();
                }}
              >
                Logout
              </button>
            </div>
          </>
        ) : (
          <>
            <h2 className="modal__title">Welcome to Sathi</h2>
            <div className="modal__actions">
              <button className="modal__btn modal__btn--primary">
                Login
              </button>
              <button className="modal__btn modal__btn--secondary">
                Sign Up
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
