import { defineStore } from 'pinia'

export const useTrekStore = defineStore('trekSearch', {
  state: () => ({
    searchQuery: '',
    filterDifficulty: '',
    currentPage: 1
  }),
  actions: {
    // We create actions to update the state.
    // Notice how changing the search or filter automatically resets the page to 1!
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