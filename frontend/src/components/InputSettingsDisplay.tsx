import React from "react";
import { useState, useEffect } from "react";
import { Setting } from "../interfaces";
import { socket } from "../Socket";
import useStartScoreCount from "../hooks/useStartScoreCount";

function InputSettingsDisplay(props: any) {
  const [allSettings, setAllSettings] = useState<Setting[]>([]);
  const [checkedSettings, setCheckedSettings] = useState<boolean[]>([]);
  const { count, increment, decrement } = useStartScoreCount(10);

  useEffect(() => {
    socket.emit("fetch_all_settings");
    socket.on("receive_settings", function (data: any) {
      setAllSettings(data.allSettings);
      setCheckedSettings(new Array(data.allSettings.length).fill(false));
    });
  }, []);

  const confirmSettings = () => {
    socket.emit("confirm_settings", props.gameCode, checkedSettings, count);
  };

  const updateSettings = (position: number) => {
    const updatedCheckedSettings = checkedSettings.map((item, index) =>
      index === position ? !item : item
    );

    setCheckedSettings(updatedCheckedSettings);
  };

  return (
    <div className="settings-container">
      <h1>Settings</h1>
      <hr className="line"></hr>
      <div className="pick-score-container">
        <div className="settings-headers">Score</div>
        <div className="pick-score-buttons-and-label">
          <button className="pick-score-button" onClick={decrement}>
            -
          </button>
          <div className="pick-score-label">{count}</div>
          <button className="pick-score-button" onClick={increment}>
            +
          </button>
        </div>
      </div>
      <hr className="line"></hr>
      <div className="checkbox-container">
        <div className="settings-headers">Card categories</div>
        {allSettings.map(({ description }, index) => {
          return (
            <div key={index}>
              <input
                className="settings-checkbox"
                type="checkbox"
                id={`custom-checkbox-${index}`}
                name={description}
                value={description}
                checked={checkedSettings[index]}
                onChange={() => updateSettings(index)}
              />
              <label
                className="settings-checkbox-label"
                htmlFor={`custom-checkbox-${index}`}
              >
                {description}
              </label>
            </div>
          );
        })}
      </div>
      <hr className="line"></hr>

      <button
        className="confirm-settings"
        onClick={() => {
          confirmSettings();
        }}
      >
        Confirm
      </button>
    </div>
  );
}

export default InputSettingsDisplay;
