import concurrent.futures
import time
import os

from image_processor import process_single_image


def run_parallel_futures(input_dir, output_dir, num_cores):

    images = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith(('.jpg', '.png', '.jpeg'))
    ]

    if not images:
        print("No images found.")
        return

    print("=== PARADIGM B: CONCURRENT FUTURES ===")
    print(f"Images: {len(images)} | Cores: {num_cores}")

    start = time.time()

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_cores) as executor:
        futures = [
            executor.submit(process_single_image, img, output_dir)
            for img in images
        ]

        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    end = time.time()

    print(f"Success: {results.count(True)}/{len(results)}")
    print(f"Execution Time: {end - start:.4f} seconds")


if __name__ == "__main__":
    INPUT_DIR = "input2000"
    OUTPUT_DIR = "output2000"

    CORES = os.cpu_count()
    run_parallel_futures(INPUT_DIR, OUTPUT_DIR, CORES)
