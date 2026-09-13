import { useState } from "react";
import "./App.css";

const API_ORIGIN = "http://127.0.0.1:8000";
const GENERATE_URL = `${API_ORIGIN}/content/generate`;
const REGENERATE_IMAGE_URL = `${API_ORIGIN}/content/regenerate-image`;
const REGENERATE_CAPTION_URL = `${API_ORIGIN}/content/regenerate-caption`;

function resolveImageUrl(path) {
  return path.startsWith("http") ? path : `${API_ORIGIN}${path}`;
}

function RefreshIcon() {
  return (
    <svg
      width="15"
      height="15"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M21 12a9 9 0 1 1-2.64-6.36" />
      <polyline points="21 3 21 9 15 9" />
    </svg>
  );
}

export default function App() {
  const [status, setStatus] = useState("idle"); // idle | loading | success | error
  const [data, setData] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [imageLoading, setImageLoading] = useState(false);
  const [captionLoading, setCaptionLoading] = useState(false);

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
    setErrorMessage("");

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

  async function handleRegenerateCaption() {
    setCaptionLoading(true);
    setErrorMessage("");

    try {
      const response = await fetch(REGENERATE_CAPTION_URL, { method: "POST" });

      if (!response.ok) {
        const body = await response.json().catch(() => null);
        throw new Error(body?.detail || `Request failed with status ${response.status}`);
      }

      const result = await response.json();
      setData((prev) => ({
        ...prev,
        caption: result.caption,
        hashtags: result.hashtags,
      }));
    } catch (err) {
      setErrorMessage(err.message);
    } finally {
      setCaptionLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="glow" />

      <div className="card">
        <div className="card-header">
          <span className="wordmark">Glow Lab</span>
          <span className="badge">AI Generated</span>
        </div>

        <h1 className="headline">Turn your product into a post.</h1>
        <p className="subhead">
          One click generates a caption, hashtags, and an image from your product details.
        </p>

        <button
          className="generate-btn"
          onClick={handleGenerate}
          disabled={status === "loading"}
        >
          {status === "loading" ? (
            <>
              <span className="spinner" />
              Generating
            </>
          ) : (
            "Generate post"
          )}
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
                src={resolveImageUrl(data.image_url)}
                alt={data.product}
                className={`result-image ${imageLoading ? "result-image-loading" : ""}`}
              />
              <button
                className="icon-btn image-icon-btn"
                onClick={handleRegenerateImage}
                disabled={imageLoading}
                title="Regenerate image"
                aria-label="Regenerate image"
              >
                <RefreshIcon />
                {imageLoading ? "Regenerating…" : "Regenerate image"}
              </button>
            </div>

            <p className="result-meta">
              {data.business.name}, {data.product}
            </p>

            <div className="caption-row">
              <p className="result-caption">{data.caption}</p>
              <button
                className="icon-btn caption-icon-btn"
                onClick={handleRegenerateCaption}
                disabled={captionLoading}
                title="Regenerate caption"
                aria-label="Regenerate caption"
              >
                <RefreshIcon />
              </button>
            </div>

            <div className={`hashtags ${captionLoading ? "hashtags-loading" : ""}`}>
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