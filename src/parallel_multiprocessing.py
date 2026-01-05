import multiprocessing
import time
import os

from image_processor import process_single_image


def run_parallel_multiprocessing(input_dir, output_dir, num_cores):

    images = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith(('.jpg', '.png', '.jpeg'))
    ]

    if not images:
        print("No images found.")
        return

    print("=== PARADIGM A: MULTIPROCESSING ===")
    print(f"Images: {len(images)} | Cores: {num_cores}")

    tasks = [(img, output_dir) for img in images]

    start = time.time()

    with multiprocessing.Pool(processes=num_cores) as pool:
        results = pool.starmap(process_single_image, tasks)

    end = time.time()

    print(f"Success: {results.count(True)}/{len(results)}")
    print(f"Execution Time: {end - start:.4f} seconds")


if __name__ == "__main__":
    INPUT_DIR = "input2000"
    OUTPUT_DIR = "output2000"

    CORES = multiprocessing.cpu_count()
    run_parallel_multiprocessing(INPUT_DIR, OUTPUT_DIR, CORES)
