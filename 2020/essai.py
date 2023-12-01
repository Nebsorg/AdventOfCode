import time


def main():

    with open("Z:\donnees\developpement\Python\AdventOfCode\day13_test.txt", 'r') as f:
        lines = [line.strip() for line in f.readlines()]

        # Part 1
        start = int(lines[0])
        ids = lines[1].split(',')
        bus_ids = [int(i) for i in ids if i != 'x']
        best_id = 0
        wait_time = 10000000
        for bus in bus_ids:
            w = bus - start % bus
            if w < wait_time:
                wait_time = w
                best_id = bus
        print(f"Best bus is {best_id}, I will wait {wait_time} minutes. Answer is = {best_id*wait_time}")

        # Part 2
        buses_pos = []
        for i in range(0, len(ids)):
            if ids[i] != 'x':
                buses_pos.append((int(ids[i]), i))
        ans = 0
        step = 1  # Step must be divisible by past buses
        print(buses_pos)
        for i in range(0, len(buses_pos)):
            while (ans + buses_pos[i][1]) % buses_pos[i][0] != 0:
                ans += step  # Adding this step does not compromise previous buses
            step *= buses_pos[i][0]
        print(f"Answer = {ans}")


if __name__ == "__main__":
    tic = time.perf_counter()
    main()
    toc = time.perf_counter()
    print(f"Done in {toc - tic:0.3f}s")
