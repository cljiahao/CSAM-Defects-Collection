import React, { useState, useEffect, useRef, useContext } from "react";
import { AppContext } from "../../../contexts/context";
import { mouse_delta, initialDisplay } from "../../../ini";

import ChipMarker from "../components/Canvas";

const PanAndZoom = ({ highlight }) => {
  const { array, focus, state, setFocus } = useContext(AppContext);
  const [isPanning, setPanning] = useState(false);
  const [moved, setMove] = useState(false);
  const [container, setContainer] = useState();
  const [display, setDisplay] = useState(initialDisplay);
  const containerRef = useRef();

  useEffect(() => {
    if (focus.state === true) {
      const rect = containerRef.current.getBoundingClientRect();
      setDisplay({
        ...display,
        x:
          (rect.width / 2 - (focus.x * rect.width) / container.width) *
          focus.scale,
        y:
          (rect.height / 2 - (focus.y * rect.height) / container.height) *
          focus.scale,
        scale: focus.scale,
      });
    } else {
      setDisplay({ ...display, x: focus.x, y: focus.y, scale: focus.scale });
    }
  }, [focus]);

  useEffect(() => {
    const onMouseUp = () => {
      setPanning(false);
    };
    const onMouseMove = (e) => {
      if (isPanning) {
        setDisplay({
          ...display,
          x: display.x + e.clientX - display.oldX,
          y: display.y + e.clientY - display.oldY,
          oldX: e.clientX,
          oldY: e.clientY,
        });
        const diffx = Math.abs(display.x + e.clientX - display.oldX);
        const diffy = Math.abs(display.y + e.clientY - display.oldY);
        if (mouse_delta < diffx && mouse_delta < diffy) setMove(false);
      }
    };

    window.addEventListener("mouseup", onMouseUp);
    window.addEventListener("mousemove", onMouseMove);
    return () => {
      window.removeEventListener("mouseup", onMouseUp);
      window.removeEventListener("mousemove", onMouseMove);
    };
  });

  const onMouseDown = (e) => {
    e.preventDefault();
    setPanning(true);
    setMove(true);
    setDisplay({
      ...display,
      oldX: e.clientX,
      oldY: e.clientY,
    });
  };

  const onWheel = (e) => {
    if (e.deltaY) {
      const sign = Math.sign(e.deltaY) / 10;
      const scale = 1 - sign;
      const rect = containerRef.current.getBoundingClientRect();
      if (display.scale >= 1) {
        setDisplay({
          ...display,
          x: display.x * scale - (rect.width / 2 - e.clientX + rect.x) * sign,
          y:
            display.y * scale -
            ((container.height * rect.width) / container.width / 2 -
              e.clientY +
              rect.y) *
              sign,
          scale: display.scale * scale,
          width: rect.width,
          height: rect.height,
        });
      } else setDisplay({ ...display, x: 0, y: 0, scale: 1 });
    }
  };

  const resetFocus = () => {
    setFocus({
      ...focus,
      state: false,
      x: 0,
      y: 0,
      scale: 1,
    });
  };

  const onLoad = (e) => {
    setContainer({
      width: e.target.naturalWidth,
      height: e.target.naturalHeight,
    });
    const rect = containerRef.current.getBoundingClientRect();

    setDisplay({
      oldX: 0,
      oldY: 0,
      x: 0,
      y: 0,
      scale: 1,
      width: rect.width,
      height: rect.height,
    });
  };

  return (
    <div
      className="holder"
      ref={containerRef}
      onMouseDown={onMouseDown}
      onWheel={onWheel}
      onDoubleClick={resetFocus}
    >
      <div
        style={{
          transform: `translate(${display.x}px, ${display.y}px) scale(${display.scale})`,
        }}
      >
        {array.chips && (
          <ChipMarker moved={moved} display={display} highlight={highlight} />
        )}
        <img
          className="image_cont"
          src={state.image.src}
          alt={state.image.alt}
          onLoad={onLoad}
        />
      </div>
    </div>
  );
};

export default PanAndZoom;
