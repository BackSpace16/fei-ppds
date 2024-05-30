from time import perf_counter
import asyncio
import aiohttp


async def dwnld_file(session, url, file):    
    async with session.get(url+file) as response:
        print(response)


async def main():
    dwnld_url = "https://ploszek.com/ppds/"
    dwnld_files = [
        "2024-01.uvod_do_paralelnych_a_distribuovanych_vypoctov.pdf",
        "2024-02.mutex%20multiplex%20randezvouse%20bariera.pdf",
        "2024-03.zrychlenie_pk_rw_fajciari.pdf",
        "2024-04.Paralelne_vypocty_1.pdf",
        "2024-05.1.Paralelne_vypocty_2.pdf",
        "2024-05.2.Paralelne_vypocty_2.pdf",
        "2024-06.Paralelne_vypocty_3.pdf",
        "2024-08.cuda.pdf",
        "2024-11.async.pdf",
        "2024-12.async2.pdf"
    ]
    time_start = perf_counter()

    async with aiohttp.ClientSession() as session:
        tasks = list()
        for file in dwnld_files:
            tasks.append(dwnld_file(session, dwnld_url, file))

        await asyncio.gather(*tasks)

    time_elapsed = perf_counter() - time_start
    print(f"Total time elapsed: {time_elapsed:.4f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())
