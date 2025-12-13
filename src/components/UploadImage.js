import { useContext, useState } from "react";
import { upload } from "../services/api";
import { AuthContext } from "../context/AuthContext";

export default function UploadImage({ endpoint = "/upload/car", onUploaded }) {
  const { token } = useContext(AuthContext);
  const [preview, setPreview] = useState("");

  const handle = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const res = await upload(endpoint, file, token);
    setPreview(res.url);
    onUploaded(res.url);
  };
  return (
    <div>
      <input type="file" accept="image/*" onChange={handle} />
      {preview && <img src={preview} alt="preview" style={{ width: 160, marginTop: 8, borderRadius: 8 }} />}
    </div>
  );
}
