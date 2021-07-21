# botbot
: 디코이드 채널에 챗봇 생성하기

1. https://discord.com/developers/applications 페이지에서 bot token 생성하기
2. https://developers.kakao.com/ 페이지에서 다음 검색 API 이용을 위한 token 생성

In dicobot.py
```
discord_key = 'discord_key'
kakao_key = 'kakao_key'
```
값 변경하여 사용

---------------------------------------------------------------------------

<h3>챗봇 기능 설명</h3>

<strong>$안녕!! or $hello</strong>
>>"방가워! \(@^0^@)/"

<strong>$bye</strong>
>>"작별인사 하지마!!! (ノ｀Д)ノ"

<strong>$게시판조회</strong>
>>app.py의 "/board" url 출력

<strong>$게시판작성</strong>
>>app.py의 "/board" url에 데이터 입력

