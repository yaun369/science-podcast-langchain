# LangChain➕OpenAI➕TTS 把论文制作成播客

## 实现

1. 解析PDF格式论文并且切块
2. 使用OpenAI Embedding API处理论文切块内容
3. 使用Chroma持久化得到的Embeddings结果
4. 利用ChatGPT对论文内容提问
5. 在持久化数据中搜索最相关的内容
6. 组合最相关的结果，整理成prompt再向ChatGPT提问
7. 把返回的文本结果合成语音
8. 拼接提问和回答音频制作成播客