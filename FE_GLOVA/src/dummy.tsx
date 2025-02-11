import { Badge, Book } from "./api/api";

export const dummy_book: Book[] = [
  {
    date: "2025-02-07",
    time: "12:30",
    bookTitle: "소년이 온다",
    bookImage: "../../image_data/book.jpg",
    questionText: "국내에서 노벨 문학상을 받은 책이 있는거 알아?",
  },
];

export const dummy_Home4 = {
  bookTitle: "소년이 온다",
  bookimage: "../../image_data/book.jpg",
  description: "'소년이 온다'는 광주 민주화 운동을 배경으로 한강 작가가 쓴 깊이 있는 작품으로, 인간의 고통과 기억을 섬세하게 그려냈습니다. 해외에서도 큰 주목을 받아 여러 문학상을 수상했으며, 노벨문학상 후보로도 거론된 바 있습니다. 비록 국내에서 노벨문학상을 받은 작품은 없지만, 이 책은 그만큼 의미 있고 강렬한 울림을 주는 작품입니다.",
  question: "국내에서 노벨문학상을 받은 책이 있는거 알아?"
}


export const dummyBadges: Badge[] = [
  {
    createdAt: "2025-02-08T10:30:00Z",
    badgeImage: "../../image_data/badges/b1.png",
    bookTitle: "해리 포터와 마법사의 돌"
  },
  {
    createdAt: "2025-02-07T15:20:00Z",
    badgeImage: "../../image_data/badges/b2.png",
    bookTitle: "어린 왕자"
  },
  {
    createdAt: "2025-02-06T08:45:00Z",
    badgeImage: "../../image_data/badges/b3.png",
    bookTitle: "이상한 나라의 앨리스"
  },
  {
    createdAt: "2025-02-05T18:10:00Z",
    badgeImage: "../../image_data/badges/b4.png",
    bookTitle: "셜록 홈즈: 바스커빌 가의 개"
  }
];

export const Nodata: Book[] = [
  {
    date: "2000-01-01",
    time: "00:00",
    bookTitle: "책을 추천받아 보세요!",
    bookImage: "../../image_data/Library_sample.png",
    questionText: "추천 받은 책에 대한 후기를 다른 사람들과 공유할 수 있어요!",
  }
];