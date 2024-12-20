<template>
  <div class="app">
    <h1>Question and Answer</h1>

    <form @submit.prevent="submitQuestion">
      <label for="question">Enter your question:</label>
      <input
        id="question"
        v-model="question"
        type="text"
        placeholder="Type your question here..."
        required
      />
      <button type="submit">Submit</button>
    </form>

    <div v-if="isLoading" class="loading">Loading answer...</div>

    <div v-if="answers.length > 0" class="answers">
      <h2>Answer:</h2>
      <div v-for="(answer, index) in answers" :key="index" class="answer">
        {{ answer }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      question: "Research AI agents and write a brief report about them.",
      answers: [],
      isLoading: false,
      eventSource: null,
    };
  },
  methods: {
    submitQuestion() {
      if (!this.question.trim()) return;

      this.answers = [];
      this.isLoading = true;

      if (this.eventSource) {
        this.eventSource.close();
      }

      const url = `http://192.168.6.93:4080/rest/v1/question?question=${encodeURIComponent(
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
  max-width: 600px;
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
}

.answer {
  background: #f0f0f0;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
}

.loading {
  color: #007bff;
}
</style>
