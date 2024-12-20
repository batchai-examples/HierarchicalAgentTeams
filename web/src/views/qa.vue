<template>
  <div class="app">
    <h1>Ask a Question</h1>

    <form @submit.prevent="submitQuestion">
      <label for="question">Your question:</label>
      <input
        id="question"
        v-model="question"
        type="text"
        placeholder="Type your question here..."
        required
      />
      <button type="submit">Submit</button>
    </form>

    <h2>Response:</h2>
    <div v-if="isLoading" class="loading">Thinking ...</div>
    <div class="answer" v-html="formattedAnswers" ref="answersContainer"></div>
  </div>
</template>

<script>
import { marked } from "marked";

export default {
  data() {
    return {
      question: "Research AI agents and write a brief report about them.",
      answers: [],
      isLoading: false,
      eventSource: null,
    };
  },
  computed: {
    formattedAnswers() {
      // Combine all answers into one Markdown string and render to HTML
      const result = this.answers.join("").replace(/\\n/g, "\n");
      return marked.parse(result);
    },
  },
  methods: {
    submitQuestion() {
      if (!this.question.trim()) return;

      this.answers = [];
      this.isLoading = true;

      if (this.eventSource) {
        this.eventSource.close();
      }

      const url = `${import.meta.env.VITE_API_ENDPOINT}/rest/v1/question?question=${encodeURIComponent(
        this.question
      )}`;
      this.eventSource = new EventSource(url);

      this.eventSource.onmessage = (event) => {
        const data = event.data;

        if (data === "[DONE]") {
          this.isLoading = false;
          this.eventSource.close();
          this.eventSource = null;
        } else {
          this.answers.push(data);
          this.scrollToBottom(); 
        }
      };

      this.eventSource.onerror = () => {
        console.error("SSE connection error");
        this.isLoading = false;
        if (this.eventSource) {
          this.eventSource.close();
          this.eventSource = null;
        }
      };
    },
    scrollToBottom() {
      // Scroll the answers container to the bottom
      this.$nextTick(() => {
        const container = this.$refs.answersContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },
  },
  beforeUnmount() {
    if (this.eventSource) {
      this.eventSource.close();
    }
  },
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f9f9f9;
}

.app {
  max-width: 1000px;
  margin: 50px auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

form {
  margin-bottom: 20px;
}

input {
  width: calc(100% - 100px);
  padding: 8px;
  margin-right: 10px;
}

button {
  padding: 8px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.answers {
  margin-top: 20px;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 4px;
  background: #f9f9f9;
}

.answer {
  background: #f0f0f0;
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
  border-radius: 4px;
  word-wrap: break-word;
  white-space: pre-wrap;
  line-height: 1.2;
  font-size: 16;
}
.loading {
  color: #007bff;
}
</style>
