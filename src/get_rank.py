# 获取自己的rank，（代码尚未生效）
# https://gitstar-ranking.com/guofei9987


from bs4 import BeautifulSoup
import requests

r = requests.get('https://gitstar-ranking.com/guofei9987')
soup = BeautifulSoup(r.text, 'lxml')

# %%
div1, = soup.find_all(name='div', attrs={'id': 'user_profile'})

div2 = div1.find_all(name='div', attrs={'class': 'row'})

star1, rank1 = div2[0], div2[1]

# %%

star = star1.find_all(name='div', attrs={'class': 'user_value col-xs-9'})[0].text.strip()

rank = rank1.find_all(name='div', attrs={'class': 'user_value col-xs-7'})[0].text.strip()

print(star, rank)

with open('data/rank.svg', 'w') as f:
    f.write(f'''<svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" width="100" height="20" role="img">
  <text x="0" y="15" style="fill:red">rank={rank}
  </text>
</svg>''')