<template>
    <div>
        <div class="d-flex justify-content-between mb-4 gap-3">

            <input type="text" class="form-control shadow-sm border-0" placeholder="Search treks by name or location..."
                :value="trekStore.searchQuery" @input="onSearchInput">

            <select class="form-select w-auto shadow-sm border-0" :value="trekStore.filterDifficulty"
                @change="onFilterChange">
                <option value="">Difficulty: All</option>
                <option value="Easy">Easy</option>
                <option value="Moderate">Moderate</option>
                <option value="Hard">Hard</option>
            </select>

        </div>

        <div class="row g-4">
            <div class="col-md-4" v-for="trek in availableTreks" :key="trek.id">
                <div class="card h-100 shadow-sm border-0">
                    <img src="https://images.unsplash.com/photo-1551632811-561732d1e306?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dHJla2tpbmd8ZW58MHx8MHx8fDA%3D"
                        class="card-img-top" alt="Trek">
                    <div class="card-body">
                        <h6 class="card-title fw-bold">{{ trek.name }}</h6>
                        <p class="text-muted small mb-2">{{ trek.location }}</p>
                        <p class="small mb-2">{{ trek.difficulty }} - {{ trek.duration }} Days</p>
                        <p class="small text-danger fw-bold">Slots Left: {{ trek.slots }}</p>
                        <button class="btn btn-outline-primary w-100" ">View Details</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="d-flex justify-content-center mt-5" v-if="totalPages > 1">
            <ul class="pagination">

                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                    <button class="page-link" @click="changePage(currentPage - 1)">&lt;</button>
                </li>

                <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
                    <button class="page-link" @click="changePage(page)">{{ page }}</button>
                </li>

                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                    <button class="page-link" @click="changePage(currentPage + 1)">&gt;</button>
                </li>

            </ul>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useTrekStore } from '../../stores/trekStore' // Import your new store

export default {
    setup() {
        const trekStore = useTrekStore();
        return { trekStore };
    },
    data() {
        return {
            availableTreks: [],
            totalPages: 1,
            searchTimeout: null // Used for debouncing
        }
    },
    mounted() {
        // When the component loads, it will use whatever is saved in the store!
        this.fetchOpenTreks()
    },
    methods: {
        async fetchOpenTreks() {
            try {
                const res = await axios.get('http://127.0.0.1:5000/api/user/treks', {
                    params: {
                        // Pull parameters directly from Pinia memory
                        search: this.trekStore.searchQuery,
                        difficulty: this.trekStore.filterDifficulty,
                        page: this.trekStore.currentPage,
                        per_page: 6
                    }
                })
                this.availableTreks = res.data.treks
                this.trekStore.currentPage = res.data.current_page
                this.totalPages = res.data.total_pages || 1
            } catch (err) {
                console.error("Error fetching treks", err)
            }
        },

        // THE DEBOUNCED SEARCH
        onSearchInput(event) {
            // 1. Update the store memory
            this.trekStore.updateSearch(event.target.value);

            // 2. Clear the previous timer if they are still typing
            clearTimeout(this.searchTimeout);

            // 3. Set a new timer to wait 400ms before calling the backend
            this.searchTimeout = setTimeout(() => {
                this.fetchOpenTreks();
            }, 400);
        },

        onFilterChange(event) {
            this.trekStore.updateDifficulty(event.target.value);
            this.fetchOpenTreks();
        },

        changePage(pageNumber) {
            if (pageNumber >= 1 && pageNumber <= this.totalPages) {
                this.trekStore.setPage(pageNumber);
                this.fetchOpenTreks();
            }
        }
    }
}
</script>