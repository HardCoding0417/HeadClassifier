link = soup.select('a[href^="/mgallery/board/view/"]')
headtext = soup.select('span.title_headtext')
title = soup.select('span.title_subject')
nickname = soup.select('span.nickname em')
for link, headtext, title, nickname in zip(link, headtext, title, nickname):
    link_url = 'https://gall.dcinside.com' + link['href']
    headtext_text = headtext.text
    title_text = title.text
    nickname_text = nickname.text

    print(f'글 링크: {link_url}')
    print(f'말머리: {headtext_text}')
    print(f'글 제목: {title_text}')
    print(f'닉네임: {nickname_text}')
    print('---')
