import etherscan_crawler as crawler

# get saved last block
last_block = get_last_block()

# default max block = last_block
max_block = last_block

# a page for unit
for page in range(1, 11):  # 1~10
    print('page:' + str(page))

    # get target page
    trans_list = crawler.get_trans_list(page)

    # stop flag
    stop = False

    for trans in trans_list:
        if trans['block'] <= last_block:  # stop
            stop = True
        else:
            if trans['block'] > max_block:  # set max_block
                max_block = trans['block']

        # do something

    if stop:
        if max_block != last_block:  # new block = max_block
            break

    # next page
