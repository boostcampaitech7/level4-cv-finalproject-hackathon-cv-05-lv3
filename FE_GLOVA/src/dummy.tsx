import { Badge, Book } from "./api/api";

export const dummy_book: Book[] = [
    {
      date: "2025-02-07",
      time: "12:30",
      bookTitle: "소년이 온다",
      bookimage: "../../image_data/book.jpg",
      question: "국내에서 노벨 문학상을 받은 책이 있는거 알아?",
    },
  ];

  export const dummy_Home4 = {
    bookTitle: "책 제목3",
    bookimage: "../../image_data/test3.jpg",
    description: "좀 더 나를 알고 싶은 너에게 가르쳐 줄게 \
                  너만 알고 있어 내꺼 하는 법 \
                  앞머리를 자르고 오면, 알아봐 줘 아님 삐질게 \
                  쇼트케이크 딸기는 꼭 나에게 양보해야 돼 \
                  집에 가는 길은 멀리 돌아가 줘 \
                  두근거리니까, 이 마음, 알아줘 \
                  내꺼 하는 법 \
                  내꺼 하려면 \
                  민트, 초코, 파인애플, 피자는 잘 먹어야 돼 \
                  너만 알고 있어, 내꺼 하는 법 가르쳐 줄게 \
                  조금 부끄럽고 많이 서투르니까 \
                  적극적으로 내게 다가와 줄래? \
                  말은 안 했지만 외로워하는 날 \
                  말없이 안아줘, 이 마음, 알아줘 \
                  내꺼 하는 법 \
                  내꺼 하려면 \
                  새벽에 살짝 편의점 갈 땐, 나랑 춤추며 가자 \
                  너만 알고 있어, 내꺼 하는 법 가르쳐 줄게 \
                  제멋대로에 어리광쟁이 하지만 \
                  귀여우니까, 용서, 쓰담쓰담, 해줘 \
                  내꺼 하는 법 \
                  사실은 말야 \
                  너가 나 없인 못 산다고 했잖아, 나도 똑같아 \
                  그러니까 앞으로도 내 옆에 있어 줘야 해 \
                  나도 네 거야",
    question: "옴맘마,,,,"
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
  
  export const Nodata:Book[] = [
    {
      date: "2000-01-01",
      time: "00:00",
      bookTitle: "책을 추천받아 보세요!",
      bookimage: "../../image_data/Library_sample.png",
      question: "추천 받은 책에 대한 후기를 다른 사람들과 공유할 수 있어요!",
    }
  ];