import { useState } from "react";
import "./App.css";

const GENERATE_URL = "http://127.0.0.1:8000/content/generate";
const REGENERATE_IMAGE_URL = "http://127.0.0.1:8000/content/regenerate-image";

export default function App() {
  const [status, setStatus] = useState("idle"); // idle | loading | success | error
  const [data, setData] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [imageLoading, setImageLoading] = useState(false);

  async function handleGenerate() {
    setStatus("loading");
    setErrorMessage("");

    try {
      const response = await fetch(GENERATE_URL, { method: "POST" });

      if (!response.ok) {
        const body = await response.json().catch(() => null);
        throw new Error(body?.detail || `Request failed with status ${response.status}`);
      }

      const result = await response.json();
      setData(result);
      setStatus("success");
    } catch (err) {
      setErrorMessage(err.message);
      setStatus("error");
    }
  }

  async function handleRegenerateImage() {
    setImageLoading(true);

    try {
      const response = await fetch(REGENERATE_IMAGE_URL, { method: "POST" });

      if (!response.ok) {
        const body = await response.json().catch(() => null);
        throw new Error(body?.detail || `Request failed with status ${response.status}`);
      }

      const result = await response.json();
      setData((prev) => ({ ...prev, image_url: result.image_url }));
    } catch (err) {
      setErrorMessage(err.message);
    } finally {
      setImageLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="card">
        <p className="wordmark">Glow Lab</p>
        <h1 className="headline">Turn your product into a post.</h1>
        <p className="subhead">
          One click generates a caption, hashtags, and an image from your product details.
        </p>

        <button
          className="generate-btn"
          onClick={handleGenerate}
          disabled={status === "loading"}
        >
          {status === "loading" ? "Generating…" : "Generate post"}
        </button>

        {status === "error" && (
          <p className="error-message">
            Something went wrong generating this post: {errorMessage}
          </p>
        )}

        {status === "success" && data && (
          <div className="result">
            <div className="result-image-wrap">
              <img
                src={data.image_url}
                alt={data.product}
                className={`result-image ${imageLoading ? "result-image-loading" : ""}`}
              />
              <button
                className="regenerate-btn"
                onClick={handleRegenerateImage}
                disabled={imageLoading}
              >
                {imageLoading ? "Regenerating…" : "Regenerate image"}
              </button>
            </div>

            <p className="result-meta">
              {data.business.name}, {data.product}
            </p>
            <p className="result-caption">{data.caption}</p>
            <div className="hashtags">
              {data.hashtags.map((tag) => (
                <span className="hashtag" key={tag}>
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}