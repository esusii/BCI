try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device)
        args.samplerate = device_info['default_samplerate']
    blocksize = int(args.blocksize * args.samplerate / 1000)
    width = int(args.window * args.samplerate / (1000 * args.downsample))
    if width < 1:
        raise ValueError('Window too short')
    if blocksize == 0:
        # Set blocksize to default if not specified
        blocksize = int(args.samplerate * args.interval / 1000)
    if args.interval > 1000 * args.window:
        raise ValueError('Interval must be shorter than window')
    anim.interval = args.interval
    stream = sd.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, blocksize=blocksize,
        callback=audio_callback)
    with stream:
        anim = FuncAnimation(fig, update_plot, interval=args.interval)
        plt.show()
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
