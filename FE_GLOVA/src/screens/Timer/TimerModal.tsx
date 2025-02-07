import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "../../components/ui/button";
import { Server2Books, Book } from "../../api/api";

export const TimerModal = ({ showModal, setShowModal, onBookSelect }) => {
  const [books, setBooks] = useState<Book[]>([]);

  useEffect(() => {
    if (showModal) {
      Server2Books().then((data) => {
        setBooks(data);
      });
    }
  }, [showModal]);

  const handleBookClick = (bookImage) => {
    onBookSelect(bookImage);
    setShowModal(false);
  };

  return (
    <AnimatePresence>
      {showModal && (
        <motion.div
          className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            className="bg-white w-[350px] h-[500px] p-5 rounded-lg flex flex-col items-center justify-center relative z-50 overflow-hidden"
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="text-2xl font-bold mb-4">추천 도서</h2>
            <div className="w-full h-[380px] overflow-y-auto grid grid-cols-2 gap-4">
              {books.map((book, index) => (
                <div key={index} className="flex flex-col items-center">
                  <img
                    src={book.bookimage}
                    alt={book.bookTitle}
                    className="w-32 h-40 object-cover rounded-lg shadow-md cursor-pointer"
                    onClick={() => handleBookClick(book.bookimage)}
                  />
                  <p className="text-sm mt-2 text-center font-medium">{book.bookTitle}</p>
                </div>
              ))}
            </div>
            <Button
              onClick={() => setShowModal(false)}
              className="absolute top-2 right-2"
            >
              닫기
            </Button>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};