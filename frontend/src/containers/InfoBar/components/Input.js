import React from "react";

const Input = ({ text, onChange }) => {
  return (
    <label className="label">
      {text}
      <input
        className="input"
        type="file"
        accept=".png, .jpg, .jpeg"
        onClick={(event) => {
          event.currentTarget.value = "";
        }}
        onChange={onChange}
        hidden
      />
    </label>
  );
};

export default Input;
