#include <iostream>
#include <tuple>
#include <vector>
#include <unordered_map>
#include <limits>
#include <random>
#include <algorithm>
#include <chrono>
#include <cassert>
#include <fstream>


template<typename T, T Begin, class Func, T ...Is>
constexpr void static_for_impl(Func &&f, std::integer_sequence<T, Is...>) {
    ( f(std::integral_constant<T, Begin + Is>{}), ... );
}

template<typename T, T Begin, T End, class Func>
constexpr void static_for(Func &&f) {
    static_for_impl<T, Begin>(std::forward<Func>(f), std::make_integer_sequence<T, End - Begin>{});
}

template<class Tuple>
constexpr std::size_t tuple_size(const Tuple &) {
    return std::tuple_size<Tuple>::value;
}

template<typename T, std::size_t... Indices>
auto vectorToTupleHelper(const std::vector<T> &v, std::index_sequence<Indices...>) {
    return std::make_tuple(v[Indices]...);
}

template<std::size_t N, typename T>
auto vectorToTuple(const std::vector<T> &v) {
    assert(v.size() >= N);
    return vectorToTupleHelper(v, std::make_index_sequence<N>());
}

//                        ore,       clay,   obsidian,      geode,  ore robot, clay robot, obs. robo., geode robo, time left
typedef std::tuple<__uint32_t, __uint32_t, __uint32_t, __uint32_t, __uint32_t, __uint32_t, __uint32_t, __uint32_t, __uint32_t> skey_t;
typedef std::tuple<__uint32_t, __uint32_t, __uint32_t> scost_t;

const size_t valsPerSingleState = 200;
const size_t nVals = std::tuple_size_v<skey_t>;

static std::vector<size_t> generateRandVector(size_t size) {
    using value_type = size_t;
    // We use static in order to instantiate the random engine
    // and the distribution once only.
    // It may provoke some thread-safety issues.
    static std::uniform_int_distribution<value_type> distribution(
            std::numeric_limits<value_type>::min(),
            std::numeric_limits<value_type>::max());
    static std::default_random_engine generator(123456);

    std::vector<value_type> data(size);
    std::generate(data.begin(), data.end(), []() { return distribution(generator); });
    return data;
}

const auto zobristKeys = generateRandVector(nVals * valsPerSingleState + 1);

struct key_hash : public std::unary_function<skey_t, std::size_t> {
    std::size_t operator()(const skey_t &k) const {
        size_t h = zobristKeys.at(zobristKeys.size() - 1UL);
        static_for<std::size_t, 0, std::tuple_size_v<skey_t> >([&](auto i) {
            size_t offset = i * valsPerSingleState;
            h ^= zobristKeys[offset + std::get<i>(k)];
        });

        return h;
    }
};

struct key_equal : public std::binary_function<skey_t, skey_t, bool> {
    bool operator()(const skey_t &v0, const skey_t &v1) const {
        bool ans = true;
        static_for<std::size_t, 0, std::tuple_size_v<skey_t> >([&](auto i) {
            ans = ans && (std::get<i>(v0) == std::get<i>(v1));
        });
        return ans;
    }
};

typedef std::unordered_map<const skey_t, __uint32_t, key_hash, key_equal> statemap_t;

__uint32_t
treeSearch(const skey_t &state, const std::vector<scost_t> &costs, const scost_t &max_costs, statemap_t &hashTable,
           __uint32_t best) {
    __uint32_t ans = 0;
    const auto T = 3UL;
    auto [nOre, nClay, nObsidian, nGeode, roboOre, roboClay, roboObsidian, roboGeode, t] = state;
    if (t <= 0) {
        return nGeode;
    }
    if (t == 1) {
        return nGeode + roboGeode; // we cannot open any geode any more
    }

    // What is the best value we can achieve, if we would build a geode robot in every move from now?
    // If it is worse than our current best, then abort...
    // sum((t-i)*(roboGeode+i),i=0..t) <= best
    if (nGeode + 1.0 / 6.0 * t * (t + 1.0) * (t + 3.0 * roboGeode - 1) <= best) {
        return best;
    }

    // Do not store every state in the hash table. Nodes close to the leaf are computationally inexpensive and
    // waste a lot of memory in the has table
    if (t > T) {
        auto itr = hashTable.find(state);
        if (hashTable.end() != itr) {
            return itr->second;
        }
    }

    // It does not make sense to have more resources than we can spend. Limit them!
    if (nOre >= std::get<0>(max_costs) && nOre > t * std::get<0>(max_costs) - roboOre * (t - 1))
        nOre = t * std::get<0>(max_costs) - (t - 1) * roboOre;
    if (nClay >= std::get<1>(max_costs) && nClay > t * std::get<1>(max_costs) - (t - 1) * roboClay)
        nClay = t * std::get<1>(max_costs) - (t - 1) * roboClay;
    if (nObsidian >= std::get<2>(max_costs) && nObsidian > t * std::get<2>(max_costs) - (t - 1) * roboObsidian)
        nObsidian = t * std::get<2>(max_costs) - (t - 1) * roboObsidian;

    // Skip building certain types of robots, if we already produce a resource at a larger rate than what can possibly be consumed
    int trials_idx[4] = {3, 0, 0, 0}, counter = 1;
    if (t > 3 && roboOre < std::get<0>(max_costs)) trials_idx[counter++] = 0;
    if (t > 5 && roboClay < std::get<1>(max_costs))
        trials_idx[counter++] = 1; // does not make sense to build clay robot, if t <= 4
    if (t > 3 && roboObsidian < std::get<2>(max_costs)) trials_idx[counter++] = 2;

    //Try building different robots
    for (auto x = 0; x < counter; x++) {
        const auto &i = trials_idx[x];
        const auto &[costOre, costClay, costObsidian] = costs.at(i);
        if (costOre <= nOre && costClay <= nClay && costObsidian <= nObsidian) {
            skey_t new_state = {nOre - costOre + roboOre,
                                nClay - costClay + roboClay,
                                nObsidian - costObsidian + roboObsidian,
                                nGeode + roboGeode,
                                roboOre + (i == 0 ? 1 : 0),
                                roboClay + (i == 1 ? 1 : 0),
                                roboObsidian + (i == 2 ? 1 : 0),
                                roboGeode + (i == 3 ? 1 : 0),
                                t - 1
            };
            ans = std::max(ans, treeSearch(new_state, costs, max_costs, hashTable, ans));
        }
    };

    // Do not build any robot...
    skey_t new_state = {nOre + roboOre,
                        nClay + roboClay,
                        nObsidian + roboObsidian,
                        nGeode + roboGeode,
                        roboOre,
                        roboClay,
                        roboObsidian,
                        roboGeode,
                        t - 1
    };
    ans = std::max(ans, treeSearch(new_state, costs, max_costs, hashTable, ans));


    if (t > T)
        hashTable[state] = ans;
    return ans;
}

std::tuple<__uint32_t, __uint32_t> solve(const size_t index, const std::vector<scost_t> &costs) {
    scost_t max_costs = {0, 0, 0};
    for (auto c: costs) {
        std::get<0>(max_costs) = std::max(std::get<0>(c), std::get<0>(max_costs));
        std::get<1>(max_costs) = std::max(std::get<1>(c), std::get<1>(max_costs));
        std::get<2>(max_costs) = std::max(std::get<2>(c), std::get<2>(max_costs));
    }

    statemap_t hashTable; // Transposition table

    auto t1 = std::chrono::_V2::high_resolution_clock::now();
    auto ans1 = treeSearch({0, 0, 0, 0, 1, 0, 0, 0, 24}, costs, max_costs, hashTable, 0);
    auto t2 = std::chrono::_V2::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> ms_double = t2 - t1;
    std::cout << index << ": Opened Geodes (24 minutes): " << ans1 << ". Time: " << ms_double.count() << " ms."
              << std::endl;

    auto ans2 = 1UL;
    if (index <= 3) {
        t1 = std::chrono::_V2::high_resolution_clock::now();
        ans2 = treeSearch({0, 0, 0, 0, 1, 0, 0, 0, 32}, costs, max_costs, hashTable, 0);
        t2 = std::chrono::_V2::high_resolution_clock::now();
        ms_double = t2 - t1;
        std::cout << index << ": Opened Geodes (32 minutes): " << ans2 << ". Time: " << ms_double.count() << " ms."
                  << std::endl;
    }

    return {ans1 * index, ans2};
}

// Function to extract integers from
// the string str
std::vector<__uint32_t> extractIntegers(std::string str) {
    std::vector<__uint32_t> found;
    size_t n = str.size();

    // This variable will store each founded
    // integer temporarily
    std::string tillNow;

    for (int i = 0; i < n; i++) {

        // If current character is an integer, then
        // add it to string tillNow
        if (str[i] - '0' >= 0 and str[i] - '0' <= 9) {
            tillNow += str[i];
        }

            // Otherwise, check if tillNow is empty or not
            // If it isn't then convert tillNow to integer
            // and empty it after printing
        else {
            if (!tillNow.empty()) {
                //cout << stoi(tillNow) << ' ';
                found.emplace_back(stoi(tillNow));
                tillNow = "";
            }
        }
    }

    // if tillNow isn't empty then convert tillNow
    // to integer and print it
    if (!tillNow.empty()) {
        std::cout << stoi(tillNow) << ' ';
    }
    return found;
}

int main() {
    auto t1 = std::chrono::_V2::high_resolution_clock::now();

    std::vector<std::vector<scost_t>> allCosts;

    std::fstream new_file;
    new_file.open("../input19_1.txt", std::ios::in);

    if (!new_file.is_open()) {
        exit(EXIT_FAILURE);
    }

    std::string sa;
    size_t rowCounter = 0;
    while (getline(new_file, sa)) {
        rowCounter++;
        auto elems = extractIntegers(sa);
        assert(elems.size() == 7);
        assert(elems.at(0) == rowCounter);
        for (auto e: elems) {
            std::cout << e << " ";
        }
        std::cout << std::endl;

        scost_t robbyOre = {elems.at(1), 0, 0};
        scost_t robbyclay = {elems.at(2), 0, 0};
        scost_t robbyObsidian = {elems.at(3), elems.at(4), 0};
        scost_t robbyGeode = {elems.at(5), 0, elems.at(6)};
        std::vector<scost_t> cost = {robbyOre, robbyclay, robbyObsidian, robbyGeode};
        allCosts.emplace_back(cost);
    }
    new_file.close();

    auto index = 1UL, qualityLevelSum = 0UL, productGeodesOpen = 1UL;
    for (const auto &c: allCosts) {
        auto [ans1, ans2] = solve(index++, c);
        qualityLevelSum += ans1;
        productGeodesOpen *= ans2;
    }

    auto t2 = std::chrono::_V2::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> ms_double = t2 - t1;
    std::cout << "Total Time: " << ms_double.count() << "ms" << std::endl;
    std::cout << "Solution 19.1: " << qualityLevelSum << std::endl;
    std::cout << "Solution 19.2: " << productGeodesOpen << std::endl;
    return 0;
}



