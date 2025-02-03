import React, { useState } from "react";

interface Props {
  className: string;
}

export const Vector = ({ className }: Props): JSX.Element => {
  const [isOverlayVisible, setIsOverlayVisible] = useState(false);

  const toggleOverlay = () => {
    setIsOverlayVisible((prev) => !prev);
  };

  return (
    <>
      {/* Vector 버튼 */}
      <button
        onClick={toggleOverlay}
        className={`bg-transparent border-none p-0 ${className}`}
        aria-label="Toggle Overlay"
      >
        <svg
          className="w-9 h-6"
          fill="none"
          height="24"
          viewBox="0 0 36 24"
          width="36"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M2.00001 24C1.43334 24 0.958674 23.808 0.576007 23.424C0.19334 23.04 0.00134023 22.5653 6.89654e-06 22C-0.00132644 21.4347 0.190674 20.96 0.576007 20.576C0.96134 20.192 1.43601 20 2.00001 20H34C34.5667 20 35.042 20.192 35.426 20.576C35.81 20.96 36.0013 21.4347 36 22C35.9987 22.5653 35.8067 23.0407 35.424 23.426C35.0413 23.8113 34.5667 24.0027 34 24H2.00001ZM2.00001 14C1.43334 14 0.958674 13.808 0.576007 13.424C0.19334 13.04 0.00134023 12.5653 6.89654e-06 12C-0.00132644 11.4347 0.190674 10.96 0.576007 10.576C0.96134 10.192 1.43601 10 2.00001 10H34C34.5667 10 35.042 10.192 35.426 10.576C35.81 10.96 36.0013 11.4347 36 12C35.9987 12.5653 35.8067 13.0407 35.424 13.426C35.0413 13.8113 34.5667 14.0027 34 14H2.00001ZM2.00001 4C1.43334 4 0.958674 3.808 0.576007 3.424C0.19334 3.04 0.00134023 2.56533 6.89654e-06 2C-0.00132644 1.43467 0.190674 0.96 0.576007 0.576C0.96134 0.192 1.43601 0 2.00001 0H34C34.5667 0 35.042 0.192 35.426 0.576C35.81 0.96 36.0013 1.43467 36 2C35.9987 2.56533 35.8067 3.04067 35.424 3.426C35.0413 3.81133 34.5667 4.00267 34 4H2.00001Z"
            fill="black"
          />
        </svg>
      </button>

      {/* 오버레이 */}
      {isOverlayVisible && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          onClick={toggleOverlay} // 오버레이 클릭 시 닫기
        >
          <div
            className="bg-white p-6 rounded-lg shadow-lg"
            onClick={(e) => e.stopPropagation()} // 내부 클릭 시 닫히지 않도록 설정
          >
            <p className="text-lg font-bold">Overlay Content</p>
            <button
              onClick={toggleOverlay}
              className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </>
  );
};
