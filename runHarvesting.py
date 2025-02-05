import multiprocessing
import sys
import python.file_manager as fm
import traceback
import ROOT
import os
import subprocess32
from shutil import copyfile
import optparse
import logging
logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.DEBUG)

sentinel = -1


def data_creator(input_dir, sample_name, version, q):
    """
    Creates data to be consumed and waits for the consumer
    to finish processing
    """
    logger.info('Creating data and putting it on the queue')

    ncopied = 0
    while True:
        data = fm.listFiles(input_dir)

        for id, item in enumerate(data):
            file_name = os.path.split(item)[1]
            # print file_name
            # print id
            if sample_name in item and version+'_' in item:
                # or not os.path.isfile('{}.checked'.format(os.path.splitext(file)[0])):
                if os.path.isfile(file_name):
                    if not os.path.isfile('{}.checked'.format(os.path.splitext(file_name)[0])):
                        # logger.debug ('file {} exists but check failed...'.format(file_name))
                        remote_checksum = fm.get_checksum(item)
                        local_checksum = fm.get_checksum(file_name)
                        if remote_checksum == local_checksum:
                            logger.debug('   remote checksum for file: {} did not change...skipping for now'.format(file_name))
                            continue
                        else:
                            logger.info('   remote checksum for file: {} changed: will copy it again'.format(file_name))
                    else:
                        continue
                copy_ret = fm.copy_from_eos(input_dir=input_dir,
                                            file_name=file_name,
                                            target_file_name=file_name,
                                            dowait=True,
                                            silent=True)
                logger.debug('copy returned: {}'.format(copy_ret))
                if copy_ret == 0:
                    q.put(file_name)
                    ncopied += 1

            if ncopied > 999:
                q.put(sentinel)
                break
        if ncopied > 999:
            break


def data_checker(queue_all, queue_ready):
    """
    Consumes some data and works on it
    """
    logger.info('Checking files and putting it on the queue "queue_ready"')

    while True:
        data = queue_all.get()
        if data is sentinel:
            queue_ready.put(sentinel)
            break

        # print('data found to be processed: {}'.format(data))
        file = ROOT.TFile(os.path.join(fm.get_eos_protocol(data), data))
        if len(file.GetListOfKeys()) == 0:
            logger.info('file: {} is not OK'.format(data))
        else:
            fname = '{}.checked'.format(os.path.splitext(data)[0])
            open(fname, 'a').close()
            if not os.path.isfile('{}.hadded'.format(os.path.splitext(data)[0])):
                queue_ready.put(data)
            else:
                logger.debug('file: {} has already been hadded...skipping it'.format(data))
        file.Close()


def data_consumer(sample_name, version, queue_ready, queue_tomove):
    logger.info('Starting data consumer')
    out_file_name = 'histos_{}_{}_temp.root'.format(sample_name, version)
    new_data = []
    index = 0
    while True:
        data = queue_ready.get()

        if data is sentinel:
            queue_tomove.put(sentinel)
            break
        new_data.append(data)
        if(len(new_data) >= 20):
            logger.info('Launch hadd on {} files: '.format(len(new_data)))
            hadd_proc = subprocess32.Popen(['hadd', '-a', '-j', '2', '-k', out_file_name]+new_data, stdout=subprocess32.PIPE, stderr=subprocess32.STDOUT)
            hadd_proc.wait()
            if hadd_proc.returncode == 0:
                logger.info('   hadd succeeded with exit code: {}'.format(hadd_proc.returncode))
                logger.debug('   hadd output follows: {}'.format(hadd_proc.stdout.readlines()))
                index += 1
                for file in new_data:
                    fname = '{}.hadded'.format(os.path.splitext(file)[0])
                    open(fname, 'a').close()
                out_file_name_copy = 'histos_{}_{}_tocopy_{}.root'.format(sample_name, version, index)
                copyfile(out_file_name, out_file_name_copy)
                queue_tomove.put(out_file_name_copy)
                del new_data[:]
                logger.debug('  resetting file list for hadd operation to {}'.format(len(new_data)))
            else:
                logger.info('   hadd failed with exit code: {}'.format(hadd_proc.returncode))
                logger.debug('   hadd output follows: {}'.format(hadd_proc.stdout.readlines()))
                file = ROOT.TFile(out_file_name)
                if len(file.GetListOfKeys()) == 0:
                    logger.info('file: {} is not OK'.format(out_file_name))
                else:
                    logger.info('file: {} is OK, will retry hadding!'.format(out_file_name))
                file.Close()


def data_mover(sample_name, version, out_dir, queue_tomove):
    logger.info('Starting data mover')
    while True:
        data = queue_tomove.get()
        if data is sentinel:
            break
        out_file_name = 'histos_{}_{}t.root'.format(sample_name, version)
        fm.copy_to_eos(data, out_dir, out_file_name)


def main():

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--input-dir',
                      dest='INPUTDIR',
                      help='input directory (can be an EOS path)')
    parser.add_option('-s', '--sample-name',
                      dest='SAMPLENAME',
                      help='name of the sample (part of the file-name)')
    parser.add_option('-v', '--version',
                      dest='VERSION',
                      help='version of the processing (part of the filename)')
    parser.add_option('-o', '--output-dir',
                      dest='OUTPUTDIR',
                      help='output directory (can be an EOS path)')

    global opt, args
    (opt, args) = parser.parse_args()

    input_dir = opt.INPUTDIR
    version = opt.VERSION
    sample_name = opt.SAMPLENAME
    out_dir = opt.OUTPUTDIR

    logger.info('Starting...')

    q = multiprocessing.Queue()
    queue_ready = multiprocessing.Queue()
    queue_tomove = multiprocessing.Queue()
    # r1 = pool.apply_async(func=data_creator, args=(input_dir, sample_name, version, q))
    # r2 = pool.apply_async(func=data_checker, args=(q, queue_ready))
    processes = []
    processes.append(multiprocessing.Process(target=data_creator,
                                             args=(input_dir, sample_name, version, q)))
    processes.append(multiprocessing.Process(target=data_checker,
                                             args=(q, queue_ready)))
    processes.append(multiprocessing.Process(target=data_consumer,
                                             args=(sample_name, version, queue_ready, queue_tomove)))
    processes.append(multiprocessing.Process(target=data_mover,
                                             args=(sample_name, version, out_dir, queue_tomove)))

    for proc in processes:
        proc.start()

    q.close()
    q.join_thread()
    queue_ready.close()
    queue_ready.join_thread()
    queue_tomove.close()
    queue_tomove.join_thread()

    for proc in processes:
        proc.join()
    return 0


if __name__ == '__main__':
    try:
        status = main()
        sys.exit(status)
    except Exception as inst:
        print (str(inst))
        print ("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc()
        sys.exit(100)
