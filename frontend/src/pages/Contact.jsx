import './Pages.css';

export default function Contact() {
  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Connect to backend
  };

  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">Contact Us</h1>
        <p className="page__subtitle">
          Have questions, feedback, or want to contribute data? Reach out to us.
        </p>
      </div>

      <form className="contact-form" onSubmit={handleSubmit}>
        <div className="contact-form__group">
          <label className="contact-form__label" htmlFor="contact-name">
            Name
          </label>
          <input
            id="contact-name"
            className="contact-form__input"
            type="text"
            placeholder="Your name"
            required
          />
        </div>

        <div className="contact-form__group">
          <label className="contact-form__label" htmlFor="contact-email">
            Email
          </label>
          <input
            id="contact-email"
            className="contact-form__input"
            type="email"
            placeholder="you@example.com"
            required
          />
        </div>

        <div className="contact-form__group">
          <label className="contact-form__label" htmlFor="contact-message">
            Message
          </label>
          <textarea
            id="contact-message"
            className="contact-form__textarea"
            placeholder="How can we help?"
            required
          />
        </div>

        <button className="contact-form__submit" type="submit">
          Send Message
        </button>
      </form>
    </div>
  );
}
