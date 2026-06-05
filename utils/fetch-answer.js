import config from '../config/index.js';
import { search } from '../services/serpapi.js';

class OrganicResult {
  answer;

  constructor({
    answer,
  } = {}) {
    this.answer = answer;
  }
}

const fetchAnswer = async (q) => {
  if (config.APP_ENV !== 'production' || !config.SERPAPI_API_KEY) {
    console.log('[search] skipped: APP_ENV=', config.APP_ENV, 'has key=', !!config.SERPAPI_API_KEY);
    return new OrganicResult();
  }
  console.log('[search] querying:', q);
  const res = await search({ q });
  console.log('[search] response keys:', Object.keys(res.data || {}));
  const { answer_box: answerBox, knowledge_graph: knowledgeGraph, organic_results: organicResults = [] } = res.data;
  console.log('[search] organic_results count:', organicResults.length);
  let answer = organicResults[0]?.snippet || '';
  if (answerBox?.answer) answer += answerBox.answer;
  if (answerBox?.result) answer += answerBox.result;
  if (answerBox?.snippet) answer += answerBox.snippet;
  if (knowledgeGraph?.description) answer += `${knowledgeGraph.title} - ${knowledgeGraph.description}`;
  console.log('[search] answer length:', answer.length);
  return new OrganicResult({ answer });
};

export default fetchAnswer;
