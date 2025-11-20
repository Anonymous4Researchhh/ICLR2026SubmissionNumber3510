import signal
import sys
import os
from pathlib import Path
import json
import threading
from environments.besiege_interface import BesiegeEnvManager
from AgenticCodes.agentic_pipeline import AgenticPipeline
from AgenticCodes.config import BASE_PATH,DEFAULT_SAVE_ROOT,APIPATH,LEVEL_FILE_BASE,SCRIPT_PATH,LEVELMENUS
import AgenticCodes.config as global_config

import argparse

    

exit_event = threading.Event()
def signal_handler(sig, frame):
    print("\nkilling process...")
    exit_event.set()
    sys.exit(0)


def override_global_config(args: argparse.Namespace, global_config) -> argparse.Namespace:
    for k, v in vars(args).items():
        if hasattr(global_config, k):
            setattr(global_config, k, v)

def run_agentic_pipeline(use_model, task, env_num, user_input,env_loop_run_times
                         ,continue_root,skip_designer,skip_inspector,skip_refiner,block_limitations,pass_userinput_to):
    agentic_pipeline = AgenticPipeline(
        save_root=DEFAULT_SAVE_ROOT,
        model_name=use_model,
        tasks=[task] * env_num
    )
    # agentic_pipeline.exp_type="abl-no-besiege"

    
    agentic_pipeline.run(
        user_input=user_input,
        save=True,
        block_limitations=block_limitations,
        continue_root=continue_root,
        skip_designer=skip_designer,
        skip_inspector=skip_inspector,
        skip_refiner=skip_refiner,
        mcts_search_times=env_loop_run_times,
        pass_userinput_to=pass_userinput_to
    )
    agentic_pipeline._release_env_manager()
    
    

if __name__ == "__main__":    
    
    signal.signal(signal.SIGINT, signal_handler)  
    signal.signal(signal.SIGTERM, signal_handler) 

    parser = argparse.ArgumentParser(description="Run AgenticPipeline with specified parameters.")
    
    # parser.add_argument("-use_model", type=str, default="o3", help="Model name to use")
    # parser.add_argument("-task", type=str, default="jump/jump_level1", help="Task name")
    # parser.add_argument("-env_num", type=int, default=2, help="Number of environments")
    # parser.add_argument("-user_input", type=str, default="In 20m front of the machine, there is a 1m high wall, it is moving towards the machine with speed 5m/s. Design a machine that can jump over the wall.")
    # parser.add_argument("-env_loop_run_times", type=int, default=5, help="Running feedback-refine loop times")
    # parser.add_argument("-continue_root", type=str, default=None)
    # parser.add_argument("-block_limitations", type=list, default=[0,1,15,63,182,56], help="block type range required the agent to use.")
    # parser.add_argument("-skip_designer", type=bool, default=False, help="If skip designer (e.g. You have finished call designer in previous experiment)")
    # parser.add_argument("-skip_inspector", type=bool, default=False, help="If skip inspector (e.g. You have finished call inspector in previous experiment)")
    # parser.add_argument("-skip_refiner", type=bool, default=False, help="If skip refiner (e.g. You have finished call refiner in previous experiment)")
    # parser.add_argument("-WHEEL_AUTO_ON", type=bool, default=True, help="If powered wheel auto working in game")
    
    # parser.add_argument("-overwrite_levelmenu", type=bool, default=True, help="use task deafult config to overwrite prompt and block_limitations")
    
    
    # parser.add_argument("-use_model", type=str, default="kimi-k2-0711-preview", help="Model name to use")
    # parser.add_argument("-task", type=str, default="cogplate/cogplate_level0", help="Task name")
    # parser.add_argument("-env_num", type=int, default=2, help="Number of environments")
    # parser.add_argument("-user_input", type=str, default="Here is a “gear board”: a wooden tabletop made of Starting Block (0) and Wooden Blocks (1).\nOn its two diagonal corners sit a Powered Medium Cog (39) rotates clockwise and an Unpowered Large Cog (51).\nA Wooden Pole (41) is stacked on the Unpowered Large Cog to show whether it turns.\n\nYour job: ONLY use Unpowered Medium Cog (38), place ONLY 2 Unpowered Medium Cog (38) anywhere on the tabletop so that the original Unpowered Large Cog (51) starts to spin.\nYou may NOT change or remove any block that is already on the board!\n\n“gear board” json:\n[{\"id\": \"0\", \"order_id\": 0, \"parent\": -1, \"bp_id\": -1}, {\"id\": \"1\", \"order_id\": 1, \"parent\": 0, \"bp_id\": 0}, {\"id\": \"1\", \"order_id\": 2, \"parent\": 1, \"bp_id\": 2}, {\"id\": \"1\", \"order_id\": 3, \"parent\": 1, \"bp_id\": 1}, {\"id\": \"1\", \"order_id\": 4, \"parent\": 1, \"bp_id\": 4}, {\"id\": \"1\", \"order_id\": 5, \"parent\": 1, \"bp_id\": 3}, {\"id\": \"1\", \"order_id\": 6, \"parent\": 0, \"bp_id\": 2}, {\"id\": \"1\", \"order_id\": 7, \"parent\": 6, \"bp_id\": 2}, {\"id\": \"1\", \"order_id\": 8, \"parent\": 6, \"bp_id\": 1}, {\"id\": \"1\", \"order_id\": 9, \"parent\": 0, \"bp_id\": 3}, {\"id\": \"1\", \"order_id\": 10, \"parent\": 9, \"bp_id\": 4}, {\"id\": \"1\", \"order_id\": 11, \"parent\": 9, \"bp_id\": 3}, {\"id\": \"1\", \"order_id\": 12, \"parent\": 0, \"bp_id\": 1}, {\"id\": \"39\", \"order_id\": 13, \"parent\": 7, \"bp_id\": 6}, {\"id\": \"51\", \"order_id\": 14, \"parent\": 4, \"bp_id\": 6}, {\"id\": \"41\", \"order_id\": 15, \"parent\": 14, \"bp_id\": 1}]")
    # parser.add_argument("-env_loop_run_times", type=int, default=5, help="Running feedback-refine loop times")
    # parser.add_argument("-continue_root", type=str, default=None)
    # parser.add_argument("-block_limitations", type=list, default=[38,51], help="block type range required the agent to use.")
    # parser.add_argument("-skip_designer", type=bool, default=False, help="If skip designer (e.g. You have finished call designer in previous experiment)")
    # parser.add_argument("-skip_inspector", type=bool, default=False, help="If skip inspector (e.g. You have finished call inspector in previous experiment)")
    # parser.add_argument("-skip_refiner", type=bool, default=False, help="If skip refiner (e.g. You have finished call refiner in previous experiment)")
    # parser.add_argument("-WHEEL_AUTO_ON", type=bool, default=True, help="If powered wheel auto working in game")
    
    # parser.add_argument("-overwrite_levelmenu", type=bool, default=True, help="use task deafult config to overwrite prompt and block_limitations")
    
    # parser.add_argument("-use_model", type=str, default="gemini-3-pro-preview-thinking", help="Model name to use")
    # parser.add_argument("-task", type=str, default="lift/lift_level5", help="Task name")
    # parser.add_argument("-env_num", type=int, default=2, help="Number of environments")
    # parser.add_argument("-user_input", type=str, default="An elongated cube is positioned 10 meters in front of the machine, 5.6 meters above ground. Immediately in front of it, at 9.5 meters from the machine and 6 meters high, is a slender railing. This railing prevents the machine's main body from getting closer to the cube, but due to its thin profile, it does not obstruct machine parts that are below or above 6 meters from passing over.\nDesign a machine to approach the cube, and lift the cube to a height of 7.5 meters.\nNote: If your machine has mobility capabilities, we will position it in front of the cube. If your design includes a lifting mechanism and is correctly positioned, we will ensure it can approach the cube to attempt the lift.")
    # parser.add_argument("-env_loop_run_times", type=int, default=5, help="Running feedback-refine loop times")
    # parser.add_argument("-continue_root", type=str, default=None)
    # parser.add_argument("-block_limitations", type=list, default=[0,1,15,63,181,2,46], help="block type range required the agent to use.")
    # parser.add_argument("-skip_designer", type=bool, default=False, help="If skip designer (e.g. You have finished call designer in previous experiment)")
    # parser.add_argument("-skip_inspector", type=bool, default=False, help="If skip inspector (e.g. You have finished call inspector in previous experiment)")
    # parser.add_argument("-skip_refiner", type=bool, default=False, help="If skip refiner (e.g. You have finished call refiner in previous experiment)")
    # parser.add_argument("-WHEEL_AUTO_ON", type=bool, default=False, help="If powered wheel auto working in game")
    
    # parser.add_argument("-overwrite_levelmenu", type=bool, default=True, help="use task deafult config to overwrite prompt and block_limitations")
    
    
    
    
    
    parser.add_argument("-use_model", type=str, default="gemini-3-pro-preview-thinking", help="Model name to use")
    parser.add_argument("-task", type=str, default="catapult/catapult_level3", help="Task name")
    parser.add_argument("-env_num", type=int, default=2, help="Number of environments")
    parser.add_argument("-user_input", type=str, default="There is a large square - shaped area. In the center of this area, there is a square enclosure. Design a catapult within the central square enclosure that can launch a boulder (type id 36) as far as possible.")
    parser.add_argument("-env_loop_run_times", type=int, default=5, help="Running feedback-refine loop times")
    parser.add_argument("-continue_root", type=str, default=None)
    parser.add_argument("-block_limitations", type=list, default=[0,1,2,5,9,15,16,22,30,35,36,41,63], help="block type range required the agent to use.")
    parser.add_argument("-skip_designer", type=bool, default=False, help="If skip designer (e.g. You have finished call designer in previous experiment)")
    parser.add_argument("-skip_inspector", type=bool, default=False, help="If skip inspector (e.g. You have finished call inspector in previous experiment)")
    parser.add_argument("-skip_refiner", type=bool, default=False, help="If skip refiner (e.g. You have finished call refiner in previous experiment)")
    parser.add_argument("-WHEEL_AUTO_ON", type=bool, default=True, help="If powered wheel auto working in game")
    parser.add_argument("-overwrite_levelmenu", type=bool, default=True, help="use task deafult config to overwrite prompt and block_limitations")
    
    
    # parser.add_argument("-use_model", type=str, default="o3", help="Model name to use")
    # parser.add_argument("-task", type=str, default="fly/fly_level2", help="Task name")
    # parser.add_argument("-env_num", type=int, default=2, help="Number of environments")
    # parser.add_argument("-user_input", type=str, default="A 10m * 10m * 10m destination area is located 140 meters directly above the machine. A constant wind of 1m/s blows throughout the entire space in the Z+ direction. Design a machine capable of vertical flight to the destination while resisting the wind's influence.")
    # parser.add_argument("-env_loop_run_times", type=int, default=5, help="Running feedback-refine loop times")
    # parser.add_argument("-continue_root", type=str, default=None)
    # parser.add_argument("-block_limitations", type=list, default=[0,1,15,63,14,25,35], help="block type range required the agent to use.")
    # parser.add_argument("-skip_designer", type=bool, default=False, help="If skip designer (e.g. You have finished call designer in previous experiment)")
    # parser.add_argument("-skip_inspector", type=bool, default=False, help="If skip inspector (e.g. You have finished call inspector in previous experiment)")
    # parser.add_argument("-skip_refiner", type=bool, default=False, help="If skip refiner (e.g. You have finished call refiner in previous experiment)")
    # parser.add_argument("-WHEEL_AUTO_ON", type=bool, default=True, help="If powered wheel auto working in game")
    # parser.add_argument("-overwrite_levelmenu", type=bool, default=True, help="use task deafult config to overwrite prompt and block_limitations")
    
    args = parser.parse_args()
    
    pass_userinput_to=[]
    simulate_menu = LEVELMENUS[args.task]
    if "pass_userinput_to" in simulate_menu:
        pass_userinput_to = simulate_menu["pass_userinput_to"]
    
    if args.overwrite_levelmenu:
        override_global_config(args,global_config)
        args.user_input = LEVELMENUS[args.task]["deafult_prompt"]
        args.block_limitations = LEVELMENUS[args.task]["block_limitations"]
    
    run_agentic_pipeline(
        use_model=args.use_model,
        task=args.task,
        env_num=args.env_num,
        user_input=args.user_input,
        env_loop_run_times=args.env_loop_run_times,
        continue_root=args.continue_root,
        skip_designer=args.skip_designer,
        skip_inspector=args.skip_inspector,
        skip_refiner=args.skip_refiner,
        block_limitations=args.block_limitations,
        pass_userinput_to=pass_userinput_to
    )