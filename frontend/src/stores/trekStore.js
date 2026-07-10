import { defineStore } from 'pinia'

export const useTrekStore = defineStore('trekSearch', {
  state: () => ({
    searchQuery: '',
    filterDifficulty: '',
    currentPage: 1
  }),
  actions: {
    updateSearch(query) {
      this.searchQuery = query;
      this.currentPage = 1; 
    },
    updateDifficulty(difficulty) {
      this.filterDifficulty = difficulty;
      this.currentPage = 1;
    },
    setPage(page) {
      this.currentPage = page;
    }
  }
})