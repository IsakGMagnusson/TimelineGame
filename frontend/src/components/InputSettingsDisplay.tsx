import React from "react";
import { useState, useEffect } from "react";
import { Setting } from "../interfaces";
import { socket } from "../Socket";

function InputSettingsDisplay(props: any) {
  const [allSettings, setAllSettings] = useState<Setting[]>([]);
  const [checkedSettings, setCheckedSettings] = useState<boolean[]>([]);

  useEffect(() => {
    socket.emit("fetch_all_settings");
    socket.on("receive_settings", function (data: any) {
      setAllSettings(data.allSettings);
      setCheckedSettings(new Array(data.allSettings.length).fill(false));
    });
  }, []);

  const confirmSettings = () => {
    socket.emit("confirm_settings", props.gameCode, checkedSettings);
  };

  const updateSettings = (position: number) => {
    const updatedCheckedSettings = checkedSettings.map((item, index) =>
      index === position ? !item : item
    );

    setCheckedSettings(updatedCheckedSettings);
  };

  return (
    <div className="settingsContainer">
      <div className="settings">
        {allSettings.map(({ description }, index) => {
          return (
            <div key={index}>
              <input
                type="checkbox"
                id={`custom-checkbox-${index}`}
                name={description}
                value={description}
                checked={checkedSettings[index]}
                onChange={() => updateSettings(index)}
              />
              <label htmlFor={`custom-checkbox-${index}`}>{description}</label>
            </div>
          );
        })}
      </div>
      <button
        onClick={() => {
          confirmSettings();
        }}
      >
        Confirm
      </button>{" "}
    </div>
  );
}

export default InputSettingsDisplay;
