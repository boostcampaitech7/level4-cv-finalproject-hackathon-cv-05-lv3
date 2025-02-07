import React, { useState, useEffect, useRef } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { ChevronLeft } from "lucide-react";
import NaviBar from "../../components/ui/navigationbar";
import { Reviews, GetReviews, UploadReview } from "../../api/api"


export const Review = (): JSX.Element => {
  const navigate = useNavigate();
  const location = useLocation();
  const [reviews, setReviews] = useState<Reviews[]>([]);
  const [inputText, setInputText] = useState("");
  const inputRef = useRef<HTMLTextAreaElement>(null);
  
  const book = location.state || {};


  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = "auto";
      inputRef.current.style.height = inputRef.current.scrollHeight + "px";
    }
  }, [inputText]);

  {/*더미 데이터 버전*/}
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey && inputText.trim()) {
      e.preventDefault();
      setReviews([...reviews, { name: "User", text: inputText }]);
      setInputText("");
    }
  };
  
  {/*서버 통신 버전*/}
//   const handleKeyDown = async (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
//     if (e.key === "Enter" && !e.shiftKey && inputText.trim()) {
//       e.preventDefault();
//       await UploadReview(book.bookTitle, inputText);
//       const reviews = await GetReviews(book.bookTitle);
//       setReviews(reviews);
//       setInputText("");
//     }
//   };

  return (
    <div className="bg-white flex flex-row justify-center w-full">
      <div className="bg-white w-[393px] min-h-screen relative flex flex-col p-4 pb-[60px]">
        {/* Title */}
        <h1 className="font-bold text-lg border-b border-black pt-[72px]">{book.bookTitle}</h1>

        {/* Image */}
        <div className="w-full flex justify-center my-2">
          <img src={book.bookimage} alt="Book Cover" className="w-[180px] h-[240px] object-cover border" />
        </div>

        <hr className="border-t border-black mb-4" />
        <p className="font-bold text-sm pb-1">리뷰를 달아보세요!</p>

        <button
          className="w-[48px] h-[30px] bg-gray-300 flex items-center justify-left gap-2.5 p-2.5 rounded-[20px] absolute top-[20px] left text-black text-lg font-normal"
          onClick={() => navigate('/Commu', { replace: true })}
        >
          <ChevronLeft size={48} />
        </button>

        {/* Input Field */}
        <textarea
          ref={inputRef}
          placeholder="Write a review..."
          className="border px-2 py-1 w-full rounded-[5px] resize-none overflow-hidden"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        {/* Reviews */}
        <div className="mt-4 space-y-2 overflow-y-auto flex-1 pb-[48px]">
          {reviews.map((review, index) => (
            <div key={index} className="bg-gray-300 p-2 rounded w-full break-words">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-gray-400 rounded" />
                <span className="font-bold">{review.name}</span>
              </div>
              <p className="mt-1 text-sm break-words">{review.text}</p>
            </div>
          ))}
        </div>
        <div className="fixed bottom-0 w-full bg-white" >
            <NaviBar activeLabel="Community" />
        </div>
      </div>
    </div>
  );
};